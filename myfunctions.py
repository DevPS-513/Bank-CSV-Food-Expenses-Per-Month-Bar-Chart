
import re


class myfunctions():

    def __init__(self,derp):
        self=self
        derp=1

    def Find_Match_From_Keyword_List(input_string,keyword_list_dictionary,no_match_name):
        
        return_match_name=no_match_name # initialize to no match found
        used_keyword=''

        for key in keyword_list_dictionary:

            keyword_list=keyword_list_dictionary[key]

            for keyword in keyword_list:
                match=re.search(keyword,input_string)
                if(match):
                    return_match_name=key
                    used_keyword=keyword
                    break

        return return_match_name,used_keyword
