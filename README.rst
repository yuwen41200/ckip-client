CKIP Client
-----------

A Python client for the Chinese Word Segmentation System (see `ckipsvr.iis.sinica.edu.tw <http://ckipsvr.iis.sinica.edu.tw/>`_) provided by Academia Sinica Chinese Knowledge and Information Processing (CKIP) Group.

Installation
------------

Simply run tho following command:

.. code-block:: sh

    pip install ckip-client

If ``pip`` is not available, you can also `download it manually from PyPI <https://pypi.python.org/pypi/ckip-client>`_.

Example
-------

In order to use the Chinese Word Segmentation System, you should register an account on `ckipsvr.iis.sinica.edu.tw <http://ckipsvr.iis.sinica.edu.tw/>`_.
You will get the server's IP address and port number when you finish the registration process.

Replace ``CKIP_*`` with your real arguments.

.. code-block:: python

    from ckipclient import CKIPClient

    sample_text = '第二屆內地搖滾音樂祭將在 9 月 24 日登場！今年共有五十五組獨立樂團'\
                  '參與演出，包含曾獲得金曲獎的「舒米恩」、「滅火器」等，陣容十分堅強。'

    ckip = CKIPClient(CKIP_IP, CKIP_PORT, CKIP_USERNAME, CKIP_PASSWORD)
    sample_results = ckip.segment(sample_text)

    for sentence in sample_results:
        print('／'.join(' '.join(word) for word in sentence))

The code above will output:

.. code-block::

    第二 DET／屆 M／內地 N／搖滾 N／音樂 N／祭 Vt／將 ADV／在 P／9 DET／月 N／24 DET／日 M／登場 Vi／！ EXCLAMATIONCATEGORY
    今年 N／共有 Vt／五十五 DET／組 M／獨立 Vi／樂團 N／參與 Vt／演出 N／， COMMACATEGORY
    包含 Vt／曾 ADV／獲得 Vt／金曲獎 N／的 T／「 PARENTHESISCATEGORY／舒米恩 N／」 PARENTHESISCATEGORY／、 PAUSECATEGORY／「 PARENTHESISCATEGORY／滅火器 N／」 PARENTHESISCATEGORY／等 POST／， COMMACATEGORY
    陣容 N／十分 ADV／堅強 Vi／。 PERIODCATEGORY

For more details, please refer to `the documentation <http://pythonhosted.org/ckip-client/>`_.
