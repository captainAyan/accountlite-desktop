# from repository import Repository
#
# file = open('book.bk', 'r').read()
# repo = Repository.parse(file)
#
# for x in repo.meta_data_dict:
#     print(x, repo.meta_data_dict[x])
#
# for x in repo.entries:
#     print(x.stringify())
#
# for x in repo.ledgers:
#     print(x.stringify())
#
# repo.add_entry(100, 121212, "cash", "bank", "narration")
# open('book.bk', "w").write(repo.stringify())
