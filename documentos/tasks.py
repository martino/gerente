import glob
import os
import zipfile
import requests
import tempfile
from celery import shared_task
from codecs import open
from documentos.models import BaseDocument


def import_document(dg, file_path):
    file_name = file_path.split('/')[-1]

    with open(file_path) as f:
        text = f.read()

    doc = BaseDocument.objects.create(
        file_name=file_name,
        original_text=text,
        group=dg
    )
    return doc.pk

@shared_task
def import_documents(dg, url):
    print "Importing {} into {}".format(url, dg)
    all_docs_pk = []
    filename = None
    ret_code = 0
    try:
        # download zip file
        remote_filename = url.split('/')[-1]
        suffix = '.' + remote_filename.split('.')[-1]
        r = requests.get(url, stream=True)
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as f_tmp:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f_tmp.write(chunk)
                    f_tmp.flush()
            filename = f_tmp.name

        if zipfile.is_zipfile(filename):
            # if is a zip file, extract it into a temp directory
            zf = zipfile.ZipFile(filename)
            tmp_dir = tempfile.mkdtemp()
            zf.extractall(tmp_dir)
            files = glob.glob(os.path.join(tmp_dir, '*'))
            # analyze all extracted file
            # TODO handle exception if a user send binary file
            for filename in files:
                if not os.path.isdir(filename):
                    all_docs_pk.append(import_document(dg, filename))
        else:
            all_docs_pk.append(import_document(dg, filename))

    except Exception, e:
        print "Hustom something went wrong"
        print e
        BaseDocument.objects.filter(pk__in=all_docs_pk).delete()
        ret_code = 1
    finally:
        if filename is not None:
            os.remove(filename)
        dg.importing_task_id = None
        dg.save()

    return ret_code
