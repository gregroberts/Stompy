#This is the trivial case and should be outputted as
#|Col0|Col1|
#-----------
#| a  | 1  |
#| b  | 2  |
#| c  | 3  |


test_1 = {
	'a':1,
	'b':2,
	'c':3
}

test_12 = [1,2,3]

#This is the first case of nested values
#Now the top level keys have multiple values associated with them
#This translates as multiple rows per top level key (TLK)
#|Col0|Col1|
#-----------
#| a  | 1  |
#| a  | 2  | 
#| a  | 3  |
#| b  | 1  |
#| b  | 2  | 
#| b  | 3  |
#| c  | 1  |
#| c  | 2  | 
#| c  | 3  |
test_2 = {
	'a':[1,2,3],
	'b':[1,2,3],
	'c':[1,2,3],
}

#Simple variant on test 2
#|Col0|Col1|
#-----------
#| a  | 1  |
#| b  | 1  |
#| b  | 2  | 
#| b  | 3  |
#| c  | 1  |
#| c  | 2  | 

test_3 = {
	'a':[1],
	'b':[1,2,3],
	'c':[1,2]
}

#Now for something a bit more realistic and complex
#| Col0   | title  | score  | Data  | metadata |
#|---------------------------------------------|
#|items   |   A    |   1    |  1    |          |
#|items   |   A    |   1    |  2    |          |
#|items   |   A    |   1    |  3    |          |
#|items   |   B    |   2    |  4    |          |
#|items   |   B    |   2    |  5    |          |
#|items   |   B    |   2    |  6    |          |
#|metadata|        |        |       | KABLOOEY | 
#-----------------------------------------------
test_4 = {
	'items':[
		{
			"title":"A",
			"score":1,
			"Data": [1,2,3]
		},
		{
			"title":"B",
			"score":2,
			"Data": [4,5,6]
		}
	],
	"metadata": "KABLOOEY"
}

#A key point here is that col0 is always going to be col0. 
#Cols will kee being called col until we encounter a deeper object
#at which point naming is taken from keys and heirarchy is obvious
#this test should show that
#
#|  Col0   |  a    |    b     |    c    |    c.Col0    |   c.Col0.a   |   c.Col0.b  |        d.Col0    |    d.Col1 |
#|   0     |  a1   |    b1    |   see   |              |              |             |        1         |           |
#|   0     |  a1   |    b1    |   see   |              |              |             |        2         |           |
#|   0     |  a1   |    b1    |   see   |              |              |             |                  |      3    |
#|   0     |  a1   |    b1    |   see   |              |              |             |                  |      4    | 
#|   1     |  a2   |    b2    |    1    |     1        |              |             |                  |           |      
#|   1     |  a2   |    b2    |    1    |     2        |              |             |                  |           |
#|   1     |  a2   |    b2    |    1    |              |      1       |      2      |                  |           |
#
# This is going to be the stickiest of use cases


test_5 = [
	{
		"a":"a1",
		"b":"b1",
		"c": "see",
		"d":[
			[1,2],
			[3,4]
		]
	},
	{
		"a":"a2",
		"b":"b2",
		"c":[
				1,
				2,
				{
					'a':1,
					'b':2
				}
		]
	}
]



#Now for something even more testing
#
#|Col0   | title   | score   |  source.site |source.verified| source.author.has | source.author.also |    source.video lenght |
#| books | Book A  |  1      |   Google     |               |     attr          |                    |                        |
#| books | Book B  |  2      |   Amazon     |               |    otherattr      |        hasthis     |                        |
#|videos | Video A |  5      |   Google     |               |    attr           |                    |           13           |
#|videos | Video B | 100     |   Youtube    |   false       |                   |                    |                        | 

test_6 = {
	"books" : [
		{
			"title":"Book A",
			"score":1,
			"source": {
				"site":"Google",
				"author": {
					"has":"attr"
				}
			}
		},
		{
			"title":"Book B",
			"score": 2,
			"source": {
				"site":"Amazon",
				"author":{
					"has":"otherattr",
					"also":"hasthis"
				}
			}
		},

	],
	"videos": [
		{
			"title":"Video A",
			"score":5,
			"source": {
				"site":"Google",
				"author":{
					"has":"attr"
				},
				"video length":3
			}
		},
		{
			"title":"Video B",
			"score":100,
			"source": {
				"site":"Youtube",
				"verified": "false"
			}
		},
	]
}



tests = {
	"test_1":test_1,
	"test_12":test_12,
	"test_2":test_2,
	"test_3":test_3,
	"test_4":test_4,
	"test_5":test_5,
	"test_6":test_6
}