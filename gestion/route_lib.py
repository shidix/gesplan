
def route_to_json(obj):
    result = {}
    try :
        result["ref"] = "3800000471{}{}".format(obj.ini_date.year, str(obj.ref).zfill(7))
        result["ini_date"] = "{}".format(obj.ini_date.strftime("%d-%m-%Y %H:%M"))
        result["ot_nima"] = "{}".format(obj.source.nima)
        result["ot_address"] = "{}".format(obj.source.address)
        result["ot_town"] = "{}".format(obj.source.town)
        if obj.source.company_owner != None:
            result["co_nif"] = "{}".format(obj.source.company_owner.nif)
            result["co_name"] = "{}".format(obj.source.company_owner.name)
            result["co_nima"] = "{}".format(obj.source.nima)
            result["co_reg_number"] = "{}".format(obj.source.company_owner.register_number)
            result["co_address"] = "{}".format(obj.source.company_owner.address)
            result["co_cp"] = "{}".format(obj.source.company_owner.cp)
            result["co_town"] = "{}".format(obj.source.company_owner.town)
            result["co_province"] = "{}".format(obj.source.company_owner.province)
            result["co_phone"] = "{}".format(obj.source.company_owner.phone)
            result["co_email"] = "{}".format(obj.source.company_owner.email)
        if obj.source.company != None:
            result["cm_nif"] = "{}".format(obj.source.company.nif)
            result["cm_name"] = "{}".format(obj.source.company.name)
            result["cm_nima"] = "{}".format(obj.source.nima)
            result["cm_reg_number"] = "{}".format(obj.source.company.register_number)
            result["cm_address"] = "{}".format(obj.source.company.address)
            result["cm_cp"] = "{}".format(obj.source.company.cp)
            result["cm_town"] = "{}".format(obj.source.company.town)
            result["cm_province"] = "{}".format(obj.source.company.province)
            result["cm_phone"] = "{}".format(obj.source.company.phone)
            result["cm_email"] = "{}".format(obj.source.company.email)
        result["res_ler"] = "{}".format(obj.waste.ler)
        result["res_desc"] = "{}".format(obj.waste.description)
        result["res_treatment_code"] = "{}".format(obj.waste.treatment.code)
        result["res_treatment_desc"] = "{}".format(obj.waste.treatment.description)
        result["res_op_code"] = "{}".format("")
        result["res_amount"] = "{}".format(obj.weight)
        result["trans_plate"] = "{}".format(obj.truck.number_plate)
        result["trans_nif"] = "{}".format(obj.truck.company.nif)
        result["trans_name"] = "{}".format(obj.truck.company.name)
        result["trans_nima"] = "{}".format("")
        result["trans_insc"] = "{}".format(obj.truck.company.register_number)
        result["trans_addr"] = "{}".format(obj.truck.company.address)
        result["trans_cp"] = "{}".format(obj.truck.company.cp)
        result["trans_town"] = "{}".format(obj.truck.company.town)
        result["trans_province"] = "{}".format(obj.truck.company.province)
        result["trans_phone"] = "{}".format(obj.truck.company.phone)
        result["trans_email"] = "{}".format(obj.truck.company.email)
    except Exception as e:
        print ("[PointRoute toJSON] %s"%(str(e)))
    return(result)


