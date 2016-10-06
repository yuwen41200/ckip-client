#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# noinspection PyUnresolvedReferences
from ckip_client import CKIPClient

CKIP_IP = '140.109.1.1'
CKIP_PORT = 1000
CKIP_USERNAME = 'foo'
CKIP_PASSWORD = 'bar'

if __name__ == '__main__':

    sample_text = '第二屆內地搖滾音樂祭將在 9 月 24 日登場！今年共有五十五組獨立樂團'\
                  '參與演出，包含曾獲得金曲獎的「舒米恩」、「滅火器」等，陣容十分堅強。'

    ckip = CKIPClient(CKIP_IP, CKIP_PORT, CKIP_USERNAME, CKIP_PASSWORD)
    sample_results = ckip.segment(sample_text)

    for sentence in sample_results:
        print('／'.join(' '.join(word) for word in sentence))

'''
program output:

第二 DET／屆 M／內地 N／搖滾 N／音樂 N／祭 Vt／將 ADV／在 P／9 DET／月 N／24 DET／日 M／登場 Vi／！ EXCLAMATIONCATEGORY
今年 N／共有 Vt／五十五 DET／組 M／獨立 Vi／樂團 N／參與 Vt／演出 N／， COMMACATEGORY
包含 Vt／曾 ADV／獲得 Vt／金曲獎 N／的 T／「 PARENTHESISCATEGORY／舒米恩 N／」 PARENTHESISCATEGORY／、 PAUSECATEGORY／
「 PARENTHESISCATEGORY／滅火器 N／」 PARENTHESISCATEGORY／等 POST／， COMMACATEGORY
陣容 N／十分 ADV／堅強 Vi／。 PERIODCATEGORY
'''
