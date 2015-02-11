import glob
import os
import zipfile
import requests
import tempfile
import fnmatch
from celery import shared_task
from codecs import open
from documentos.models import BaseDocument


def import_document(dg, file_path):
    print "Import doucment {}".format(file_path)
    file_name = file_path.split('/')[-1]

    with open(file_path) as f:
        text = f.read()

    try:
        text = text.encode("utf-8")
    except:
        text = text.decode('latin1').encode("utf-8")

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
        # small fixes for url download
        url = url.replace('www.dropbox', 'dl.dropbox')

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
            print "{} is a zip".format(filename)
            # if is a zip file, extract it into a temp directory
            zf = zipfile.ZipFile(filename)
            tmp_dir = tempfile.mkdtemp()
            zf.extractall(tmp_dir)
            files = []
            for root, dirnames, filenames in os.walk(tmp_dir):
                for fnametmp in fnmatch.filter(filenames, '*'):
                    files.append(os.path.join(root, fnametmp))

            # analyze all extracted file
            # TODO handle exception if a user send binary file
            for fname in files:
                if not os.path.isdir(fname):
                    all_docs_pk.append(import_document(dg, fname))
        else:
            all_docs_pk.append(import_document(dg, filename))

    except Exception, e:
        print "Hustom something went wrong"
        print e
        BaseDocument.objects.filter(pk__in=all_docs_pk).delete()
        ret_code = 1
    finally:
        dg.importing_task_id = None
        dg.save()
        if filename is not None:
            os.remove(filename)

    return ret_code
