# Multiple Language Support for Warbot-1.0.0.0, v. 0.0.0.1
import os
import json

#SETS
LangDefault = 'pl_PL'

#MAGIC STATES
LangSafeDefault = 'en_EN'
DefaultLanguagePackageLocalisation = 'data/modules/MultiLangSupport/defaults/LanguagePackage.json'
OneMegaByte = 1048576

#DATA:
LangAssocMapTable = {}

#FUNCTIONS, LOGIC:
def msgLangMap( a_msgId, a_langSelect = LangDefault ):
	"""Returns text associated with the given message ID from the language map table."""
	
	mapAttempt = None
	if a_langSelect in LangAssocMapTable :
		if a_msgId in LangAssocMapTable[ a_langSelect ] :
			mapAttempt = LangAssocMapTable[ a_langSelect ][ a_msgId ]
		
	if mapAttempt != None :
		return mapAttempt
	elif a_langSelect == LangSafeDefault :
		return 'ERROR: The translation map table is corrupted!'
	else :
		return msgLangMap( a_msgId, LangSafeDefault )
			
def updateLangAssocMapTable( a_localisation ) :
	"""Tries to update internal language map table by the one included in language package supplied by the provided location."""
	
	global LangAssocMapTable
	
	if os.path.exists( a_localisation ) :
		if os.path.getsize( a_localisation ) < OneMegaByte :
			with open( a_localisation, 'rb' ) as JSONLanguagePackage :
				LangAssocMapTable = json.load( JSONLanguagePackage )
			
#INITIALISATION:			
updateLangAssocMapTable( DefaultLanguagePackageLocalisation )