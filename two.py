import one


max_err = 5

err_num = 0

for i in range(10):
    url = 'http://example.webscraping.com/places/default/view/Afghanistan-%d'%i
    html = one.download(url)
    if html is None:
            err_num +=1
            if err_num == max_err:
                break

    else:
        err_num = 0
