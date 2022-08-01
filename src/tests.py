import Utils

a = Utils.parse2cmd(r"!hello world --this\ is\ an\ option yeee")
print(a.keyword)
print(a.args)
print(a.options)