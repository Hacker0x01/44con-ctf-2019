rooms = {
	'room-a' : ('Native'  , 10 , (1, 1)  , (7, 5)), 
	'room-b' : ('Web'     , 5  , (1, 6)  , (7, 5)), 
	'room-c' : ('Trivia'  , 3  , (1, 11) , (7, 5)), 
	'room-h' : ('Web'     , 10 , (14, 6) , (8, 5)), 
	'room-k' : ('Native'  , 500, (14, 11), (8, 5)), 
	'room-e' : ('Web'     , 30 , (25, 1) , (7, 5)), 
	'room-f' : ('Native'  , 50 , (25, 11), (7, 5)), 
	'room-g' : ('Trivia'  , 100, (35, 6) , (8, 5)), 
	'room-i' : ('Web'     , 120, (45, 6) , (8, 5)), 
	'room-j' : ('Native'  , 250, (55, 6) , (8, 5))
}

roomdeps = {
	'room-a' : (), 
	'room-b' : (), 
	'room-c' : (), 
	'room-h' : ('room-a', 'room-b', 'room-c'), 
	'room-k' : ('room-a', 'room-b', 'room-c'), 
	'room-e' : ('room-h', ), 
	'room-f' : ('room-h', ), 
	'room-g' : ('room-e', 'room-f'), 
	'room-i' : ('room-g', ), 
	'room-j' : ('room-i', )
}

flags = {
	'room-a' : 'I need ya, Decks. Th1s is 4 bad one, the wors7 ye7. I need the old blade runner, I need_your magic.', 
	'room-b' : 'Fiery 7he angels F311. Deep*thunder*rolled around_their shores.', 
	'room-c' : 'Chew,^if 0nly y0u could_see_what I\'ve se3n with your ey3s...', 
	'room-e' : 'Tha7\'s%%the_spirit!1!', 
	'room-f' : '7he_light that burns^twice as br1gh7 burns for half as long, 4nd you have burned so very, Very brightly, Roy.', 
	'room-g' : 'A11 7he_courage in the w0rld cannot^alter.fact.', 
	'room-h' : 'I had in mind 5ome7hing.a.little m0re~radical.', 
	'room-i' : 'Ha1f as much-but twic3 as elegant,, sweetheart.', 
	'room-j' : 'We\'re not*computers, 5ebastian, we\'re_phy5ical.', 
}

flagmap = {v : k for k, v in flags.items()}

indices = ('room-a', 'room-b', 'room-c', 'room-h', 'room-k', 'room-e', 'room-f', 'room-g', 'room-i', 'room-j')
