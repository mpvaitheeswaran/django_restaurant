
FREE_PACK_MENU_LIMIT = 20
FREE_PACK_SCAN_LIMIT = 100
def checkMenuLimit(pack):
    if pack.pack_type == 0:
        if FREE_PACK_MENU_LIMIT > pack.total_menus:
            return True
        else: 
            return False
    else:
        return True

def checkScanLimit(pack):
    if pack.pack_type == 0:
        if FREE_PACK_SCAN_LIMIT > pack.total_scans:
            return True
        else: 
            return False
    else:
        return True