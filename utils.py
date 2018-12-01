import pandas as pd

# this is SAAS algorithm translated into python
# for the original algorithm look in hei_score.saas (just a reference)


#   "kcal"         * Specifies calorie amount.                          #
#                                                                       #
#   "vtotalleg"    * Specifies the intake of total veg plus             #
#                      legumes in cup eq.                               #
#                                                                       #
#   "vdrkgrleg"    * Specifies the intake of dark green veg             #
#                      plus legumes in cup eq.                          #
#                                                                       #
#   "f_total"      * Specifies the intake of total fruit in cup eq      #
#                                                                       #
#   "fwholefrt"    * Specifies the intake of whole fruit in cup eq.     #
#                                                                       #
#   "g_whole"      * Specifies the intake of whole grain in oz. eq.     #
#                                                                       #
#   "d_total"      * Specifies the intake of total dairy in cup eq.     #
#                                                                       #
#   "pfallprotleg" * Specifies the intake of total protein              #
#                      (includes legumes) in oz. eq.                    #
#                                                                       #
#   "pfseaplantleg"  * Specifies the intake of seafood, fish and plant  #
#                      protein (includes legumes) in oz. eq.            #
#                                                                       #
#   "monopoly"       * Specifies the grams of mono fat plus poly fat.   #
#                                                                       #
#   "satfat"         * Specifies the grams of saturated fat.            #
#                                                                       #
#   "sodium"         * Specifies the mg of sodium.                      #
#                                                                       #
#   "g_refined"      * Specifies the intake of refined                  #
#                       grain in oz. eq.                                #
#                                                                       #
#   "add_sugars"     * Specifies the intake of added sugars in tsp. eq. #

def compute_hei(food_row):
    total_hei_score = 0
    food = food_row.to_dict()
    kcal = food['kcal'] # for convenience

    # compute all 13 components then add them up
    # hei_addsug = 0
    # hei_satfat = 0
    # hei_refinedgrain = 0
    # hei_sodium = 0
    # hei_fattyacid = 0
    # hei_seaplant_prot = 0
    # hei_totprot = 0
    # hei_totaldairy = 0
    # hei_wholegrain = 0
    # hei_wholefruit = 0
    # hei_totalfruit = 0
    # hei_green_and_bean = 0
    # hei_totalveg = 0

    # Thirteenth component
    addsug_perc = 0
    if kcal > 0:
        addsug_perc = 100*(food['add_sugars']*16/kcal)
    addsugmin = 6.5
    addsugmax = 26
    hei_addsug = 0
    if addsug_perc >= addsugmax:
        hei_addsug = 0
    elif addsug_perc <= addsugmin:
        hei_addsug = 10 - (10 * (addsug_perc - addsugmin) / (addsugmax - addsugmin) )

    # Twelfth component
    sfat_perc = 0
    if kcal > 0:
        sfat_perc = 100*(food['satfat']*9/kcal)
    sfatmin = 8
    sfatmax = 16
    hei_satfat = 0
    if sfat_perc >= sfatmax:
        hei_sfat = 0
    elif sfat_perc <= sfatmin:
        hei_sfat = 10
    else:
        hei_sfat = 10 - ( 10 * ( sfat_perc - sfatmin ) / (sfatmax - sfatmin) )

    # Eleventh component
    rgden = 0
    if kcal > 0:
        rgden = food['g_refined']/(kcal/1000)
    rgmin = 1.8
    rgmax = 4.3
    hei_refinedgrain = 0
    if rgden <= rgmin:
        hei_refinedgrain = 10
    elif rgden >= rgmax:
        hei_refinedgrain = 0
    else:
        hei_refinedgrain = 10 - (10*(rgden-rgmin) / (rgmax-rgmin))
    # Tenth component
    sodden = 0
    if kcal > 0:
        sodden = food['sodium']/kcal
    sodmin = 1.1
    sodmax = 2.0
    hei_sodium = 0
    if sodden <= sodmin:
        hei_sodium = 10
    elif sodden >= sodmax:
        hei_sodium = 0
    else:
        hei_sodium = 10 - (10 * (sodden - sodmin) / (sodmax - sodmin))

    # Ninth component
    faratio = 0
    hei_fattyacid = 0
    if food['satfat'] > 0:
        faratio = food['monopoly']/food['satfat']
    farmin = 1.2
    farmax = 2.5
    if food['satfat'] == 0 and food['monopoly'] == 0:
        hei_fattyacid = 0
    elif food['satfat'] == 0 and food['monopoly'] > 0:
        hei_fattyacid = 10
    elif faratio >= farmax:
        hei_fattyacid = 10
    elif faratio <= farmin:
        hei_fattyacid = 0
    else:
        hei_fattyacid = 10 * ( (faratio-farmin) / (farmax-farmin))


    # Eigth component
    seaplden = 0
    if kcal > 0:
        seaplden = food['pfseaplantleg']/(kcal/1000)
    hei_seaplant_prot = 5*(seaplden/0.8)
    if hei_seaplant_prot > 5:
        hei_seaplant_prot = 5
    if seaplden == 0:
        hei_seaplant_prot = 0

    # Seventh component
    protden = 0
    if kcal > 0:
        protden = food['pfallprotleg']/(kcal/1000)
    hei_totprot = 5*(protden/2.5)
    if hei_totprot > 5:
        hei_totprot = 5
    if protden == 0:
        hei_totprot = 0

    # Sixth component
    dairyden = 0
    if kcal > 0:
        dairyden = food['d_total']/(kcal/1000)
    hei_totaldairy = 10*(dairyden/1.3)
    if hei_totaldairy > 10:
        hei_totaldairy = 10
    if dairyden == 0:
        hei_totaldairy = 0

    # Fifth component
    wgrnden = 0
    if kcal > 0:
        wgrnden = food['g_whole']/(kcal/1000)
    hei_wholegrain = 10*(wgrnden/1.5)
    if wgrnden == 0:
        hei_wholegrain = 0

    # Fourth component
    whfrden = 0
    if kcal > 0:
        whfrden = food['fwholefrt']/(kcal/1000)
    hei_wholefruit = 5*(whfrden/0.4)
    if hei_wholefruit > 5:
        hei_wholefruit = 5
    if whfrden == 0:
        hei_wholefruit = 0

    # Third component
    frtden = 0
    if kcal > 0:
        frtden = food['f_total']/(kcal/1000)
    hei_totalfruit = 5*(frtden/0.8)
    if hei_totalfruit > 5:
        hei_totalfruit = 5
    if frtden == 0:
        hei_totalfruit = 0

    # Second component
    grbnden = 0
    if kcal > 0:
        grbnden = food['vdrkgrleg']/(kcal/1000)
    hei_green_and_bean = 5*(grbnden/0.2)
    if hei_green_and_bean > 5:
        hei_green_and_bean = 5
    if grbnden == 0:
        hei_green_and_bean = 0

    # First component
    vegden = 0
    if (kcal > 0):
        vegden = food['vtotalleg']/(kcal/1000)
    hei_totalveg = 5*(vegden/1.1)
    if hei_totalveg > 5:
        hei_totalveg = 5
    if vegden == 0:
        hei_totalveg = 0

    total_hei_score = (hei_addsug + hei_satfat + hei_refinedgrain + hei_sodium + hei_fattyacid
                       + hei_seaplant_prot + hei_totprot + hei_totaldairy + hei_wholegrain
                       + hei_wholefruit + hei_totalfruit + hei_green_and_bean + hei_totalveg) / food['totgramsunadj']

    # only want 2 decimals
    return round(total_hei_score, 2)
