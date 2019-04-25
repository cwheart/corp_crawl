db.corps.aggregate([{$group: {_id: '$area', count: {  $sum: 1 } }}])
db.corps.find({'legal_person': null}).count()
db.corps.find({'email': null}).count()
db.corps.find({'email': {'$ne': null}}).count()
db.corps.find({d101a: true, d110a: true}).count()

