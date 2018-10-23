from lib.booleanSearch import BooleanSearch


def boolean_search(index, documents):
    print("\nParsing of boolean queries is not implement so this is an example of hardcoded query.")
    print("(smíchov OR NOT praha)")
    search = BooleanSearch(index, documents)
    res = search.b_or(
            search.b_term("smíchov"),
            search.b_not(
                search.b_term("praha")
            )
          )
    for i in range(0, 9 if len(res) >= 10 else len(res)):
        print(documents[i].url)
