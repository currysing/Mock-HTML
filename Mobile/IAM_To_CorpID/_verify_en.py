# -*- coding: utf-8 -*-
# Verify the ver5ben / ver6ben pages:
# 1. local href/src targets exist
# 2. no CJK chars outside the whitelist (logo text + proper nouns kept intentionally)
# 3. basic tag-balance sanity via html.parser
import io, os, re
from html.parser import HTMLParser

ROOT = r"C:/Projects/CorpID/Mock-HTML/Mobile/IAM_To_CorpID"
DIRS = ["ver5ben", "ver6ben"]
WHITELIST = set('稅務易職學戶互通道小程序仁一有限公司')

class Checker(HTMLParser):
    VOID = {'meta','link','br','img','input','hr','path','rect','circle','ellipse','line','text'}
    def __init__(self):
        super().__init__()
        self.stack = []
        self.errors = []
    def handle_starttag(self, tag, attrs):
        if tag not in self.VOID:
            self.stack.append(tag)
    def handle_endtag(self, tag):
        if tag in self.VOID:
            return
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        elif tag in self.stack:
            while self.stack and self.stack[-1] != tag:
                self.errors.append('unclosed <%s>' % self.stack.pop())
            self.stack.pop()
        else:
            self.errors.append('stray </%s>' % tag)

ok = True
for d in DIRS:
    folder = os.path.join(ROOT, d)
    for fn in sorted(os.listdir(folder)):
        if not fn.endswith('.html'):
            continue
        path = os.path.join(folder, fn)
        text = io.open(path, encoding='utf-8').read()

        # 1. local refs
        for m in re.finditer(r'(?:href|src)="([^"#]+?)"', text):
            ref = m.group(1)
            if re.match(r'^(https?:|mailto:|javascript:)', ref):
                continue
            target = os.path.normpath(os.path.join(folder, ref))
            if not os.path.exists(target):
                print('MISSING REF', d, fn, '->', ref); ok = False

        # 2. CJK outside whitelist
        for i, line in enumerate(text.splitlines(), 1):
            for ch in line:
                if '一' <= ch <= '鿿' and ch not in WHITELIST:
                    print('CJK', d, fn, i  , repr(line[:100])); ok = False
                    break

        # 3. tag balance
        c = Checker()
        c.feed(text)
        if c.stack or c.errors:
            print('TAG ISSUES', d, fn, c.stack[:5], c.errors[:5]); ok = False

print('ALL OK' if ok else 'ISSUES FOUND')
