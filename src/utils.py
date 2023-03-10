def missing_values(data):
    for col in data.columns:
        missings = len(data[col][data[col].isnull()]) / float(len(data))
        print(col, missings)

Dict = dict({'antwerpen-caal': 'antwerpen-centraal',
             'arcades': 'arcaden/arcades',
             'beignee': 'beignée',
             'berchem-st-ag.-berchem': 'sint-agatha-berchem/berchem-sainte-agathe',
             'berzee' : 'berzée',
             'boitsfort/bosvoorde' : 'bosvoorde/boitsfort',
             'boondael/boondaal' : 'boondaal/boondael',
             'bru. airport - zaventem' : 'brussels airport - zaventem',
             'bru.-cent.' : 'brussel-centraal/bruxelles-central',
             'bru.-chap./kap.' : 'brussel-kapellekerk/bruxelles-chapelle',
             'bru.-cong.' : 'brussel-congres/bruxelles-congrès',
             'bru.-luxembg' : 'brussel-luxemburg/bruxelles-luxembourg',
             'bru.-midi/zuid' : 'brussel-zuid/bruxelles-midi',
             'bru.-noord/nord' : 'brussel-noord/bruxelles-nord',
             'bru.-schuman' : 'brussel-schuman/bruxelles-schuman',
             'bru.-west/ouest' : 'brussel-west/bruxelles-ouest',
             'chateau-de-seilles' : 'château-de-seilles',
             'chatelet' : 'châtelet',
             'chenee' : 'chênée',
             'comines/komen' : 'comines',
             'courriere' : 'courrière',
             'court-saint-etienne' : 'court-saint-étienne',
             'ecaussinnes' : 'écaussinnes',
             'enghien/edingen' : 'enghien',
             'erbisoeul' : 'erbisœul',
             'fexhe-le-ht-clocher':'fexhe-le-haut-clocher',
             'forest-est/vorst-oost' : 'vorst-oost/forest-est',
             'forest-midi/vorst-zuid' :'vorst-zuid/forest-midi',
             'forrieres' : 'forrières',
             'franiere' : 'franière',
             'germoir/mouterij' : 'mouterij/germoir',
             'haren-zuid/sud' : 'haren-sud/haren-zuid',
             'haute-flone' : 'haute-flône',
             'hennuyeres' : 'hennuyères',
             'jurbise' : 'jurbeke',
             'la louviere-centre' : 'la louvière-centre',
             'la louviere-sud' : 'la louvière-sud',
             'la roche' : 'la roche (brabant)',
             'labuissiere' : 'labuissière',
             'lessines' : 'lessen',
             'liege-carre' : 'liège-carré',
             'liege-guillemins' : 'liège-guillemins',
             'liege-saint-lambert' : 'liège-saint-lambert',
             'lonzee' : 'lonzée',
             'marche-lez-ecaussinnes' : 'marche-lez-écaussinnes',
             'mery' : 'méry',
             'mortsel-oude-god' : 'mortsel-oude god',
             'mouscron/moeskroen' : 'mouscron',
             'nameche' : 'namêche',
             'neufchateau' : 'neufchâteau',
             'ougree' : 'ougrée',
             'papignies' : 'papegem',
             'pecrot' : 'pécrot',
             'pepinster-cite' : 'pepinster-cité',
             'peruwelz' : 'péruwelz',
             'pieton' : 'piéton',
             'pont-a-celles' : 'pont-à-celles',
             'ronse/renaix' : 'ronse',
             'ruisbr.-sauvegarde' : 'ruisbroek-sauvegarde',
             'spa-geronstere' : 'spa-géronstère',
             'st-denijs-boekel' : 'sint-denijs-boekel',
             'st-denis-bovesse' : 'saint-denis-bovesse',
             'st-gen-rode/rhode-st-gen' : 'sint-genesius-rode',
             'st-ghislain' : 'saint-ghislain',
             'st-gillis' : 'sint-gillis-dendermonde',
             'st-job' : 'sint-job',
             'st-joris-weert' : 'sint-joris-weert',
             'st-katelijne-waver' : 'sint-katelijne-waver',
             'st-mariaburg' : 'sint-mariaburg',
             'st-martens-bodegem' : 'sint-martens-bodegem',
             'st-niklaas' : 'sint-niklaas',
             'st-truiden' : 'sint-truiden',
             'tour et taxis/thurn en taxis' : 'thurn en taxis/tour et taxis',
             'uccle/ukkel-calevoet' : 'ukkel-kalevoet/uccle-calevoet',
             'uccle/ukkel-stalle' : 'ukkel-stalle/uccle-stalle',
             'ville-pommeroeul' : 'ville-pommerœul',
             'vise' : 'visé',
             'vivier d\'oie/diesdelle' : 'diesdelle/vivier d\'oie',
             'watermael/watermaal' : 'watermaal/watermael',
             'yves-gomezee' : 'yves-gomezée'
             })


dict2 = dict({'arcaden' : 'arcaden/arcades',
'beignee' : 'beignée',
'berzee' :'berzée',
'beveren(waas)': 'beveren',
'boondaal': 'boondaal/boondael',
'bosvoorde': 'bosvoorde/boitsfort',
'brussel-centraal':'brussel-centraal/bruxelles-central',
'brussel-congres':'brussel-congres/bruxelles-congrès',
'brussel-kapellekerk':'brussel-kapellekerk/bruxelles-chapelle',
'brussel-luxemburg':'brussel-luxemburg/bruxelles-luxembourg',
'brussel-noord':'brussel-noord/bruxelles-nord',
'brussel-schuman':'brussel-schuman/bruxelles-schuman',
'brussel-west':'brussel-west/bruxelles-ouest',
'brussel-zuid':'brussel-zuid/bruxelles-midi',
'chateau-de-seilles':'château-de-seilles',
'chatelet':'châtelet',
'chenee':'chênée',
'komen':'comines',
'courriere':'courrière',
'court-saint-etienne':'court-saint-étienne',
'diesdelle': "diesdelle/vivier d'oie",
'edingen':'enghien',
'erbisoeul':'erbisœul',
'forrieres':'forrières',
'franiere':'franière',
'haren-zuid':'haren-sud/haren-zuid',
'haute-flone':'haute-flône',
'hennuyeres':'hennuyères',
'jurbise': 'jurbeke',
'la louviere-centre':'la louvière-centre',
'la louviere-sud':'la louvière-sud',
'la roche(brabant)':'la roche (brabant)',
'labuissiere':'labuissière',
'lessines':'lessen',
'liege-carre':'liège-carré',
'liege-guillemins':'liège-guillemins',
'liege-saint-lambert':'liège-saint-lambert',
'lonzee':'lonzée',
'marche-lez-ecaussinnes':'marche-lez-écaussinnes',
'moeskroen':'mouscron',
'mouterij':'mouterij/germoir',
'mery':'méry',
'nameche':'namêche',
'neufchateau':'neufchâteau',
'ougree':'ougrée',
'papignies':'papegem',
'pepinster-cite':'pepinster-cité',
'pieton':'piéton',
'pont-a-celles':'pont-à-celles',
'pecrot':'pécrot',
'peruwelz':'péruwelz',
'schaarbeek':'schaarbeek/schaerbeek',
'sint-agatha-berchem':'sint-agatha-berchem/berchem-sainte-agathe',
'sint-gillis(dendermonde)':'sint-gillis-dendermonde',
'spa-geronstere':'spa-géronstère',
'thurn en taxis':'thurn en taxis/tour et taxis',
'ukkel-kalevoet':'ukkel-kalevoet/uccle-calevoet',
'ukkel-stalle':'ukkel-stalle/uccle-stalle',
'ville-pommeroeul':'ville-pommerœul',
'vise':'visé',
'vorst-oost':'vorst-oost/forest-est',
'vorst-zuid':'vorst-zuid/forest-midi',
'watermaal':'watermaal/watermael',
'yves-gomezee':'yves-gomezée',
'ecaussinnes':'écaussinnes'})





