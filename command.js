db.corps.aggregate([{$group: {_id: '$area', count: {  $sum: 1 } }}])
db.corps.find({'legal_person': null}).count()