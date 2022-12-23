import requests

id = ""

collection = "0xbfc26064667edcbdeaaa488873926008db2b90e1"

nfts = []

while True:

    if id != "":
        r = requests.get('https://soonaverse.com/api/getMany?collection=nft&fieldName=collection&fieldValue=' + collection + '&startAfter=' + id)
    else:
        r = requests.get('https://soonaverse.com/api/getMany?collection=nft&fieldName=collection&fieldValue=' + collection)

    id = ""

    for x in r.json():
        id = x['id']

        if(x.get('availablePrice') is not None and x['availablePrice'] is not None):

            if(x['availablePrice'] > 1 and (x.get('saleAccessMembers') is None or len(x['saleAccessMembers']) == 0)):

                num = int(x['name'].split("#",1)[1].split(" ",1)[0])
                set_num = int((num - 1) / 3)

                nfts.append({'num': num, 'set_num': set_num, 'name': x['name'], 'availablePrice': x['availablePrice'], 'id': x['id']})

    if id=="":
        break

newlist = sorted(nfts, key=lambda d: d['num']) 

n = 0
set_count = 0

total_price = 0
nft = []
results = []

for f in newlist:

    if f['set_num'] == n:
        set_count +=1
        total_price += f['availablePrice']
        nft.append({'availablePrice': f['availablePrice'], 'name': f['name'], 'id': f['id']})
    else:  # New set
        n = f['set_num']
        set_count = 1
        total_price = f['availablePrice']
        nft = [{'availablePrice': f['availablePrice'], 'name': f['name'], 'id': f['id']}]
    
    if(set_count == 3):
        results.append({'total_price': total_price, 'nft': nft})

final_list = sorted(results, key=lambda d: d['total_price']) 

for f in final_list:
    print(f['nft'][0]['name'] + ' + ' + f['nft'][1]['name'] + ' + ' + f['nft'][2]['name'] + ' (' + str(int(f['total_price']/1000000)) + ' Mi):')
    print('  https://soonaverse.com/nft/' + f['nft'][0]['id'] + ' (' + str(int(f['nft'][0]['availablePrice']/1000000)) + ' Mi)')
    print('  https://soonaverse.com/nft/' + f['nft'][1]['id'] + ' (' + str(int(f['nft'][1]['availablePrice']/1000000)) + ' Mi)')
    print('  https://soonaverse.com/nft/' + f['nft'][2]['id'] + ' (' + str(int(f['nft'][2]['availablePrice']/1000000)) + ' Mi)')
