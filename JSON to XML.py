

import json
import xml.etree.ElementTree as ET
import xml.sax.saxutils as XMLS

"""Функция convert_json_to_xml() принимает на вход путь к JSON-файлу, который хранится на ПК, и возвращает XML-файл,
   оформленный согласно требованиям, с таким же названием как исходный JSON-файл. """

def convert_json_to_xml(json_file_path): 

    with open(json_file_path, encoding="utf-8") as json_file: #открываем JSON-файл
        data = json.load(json_file) #записываем содержимое JSON-файла в переменную data


    root = ET.Element("Entities") # корневой элемент Entities
    entity1 = ET.SubElement(root, "Entity", Type ="Location") #создаем Entity под названием Location
    entity2 = ET.SubElement(root, "Entity", Type ="Company") #создаем Entity под названием Company
    entity3 = ET.SubElement(root, "Entity", Type ="Company") #создаем Entity под названием Company
    entity4 = ET.SubElement(root, "Entity", Type ="Tinder Profile") #создаем Entity под названием Tinder Profile
    fields_for_profile = ET.SubElement(entity4, "Fields") #создаем поля для Tinder Profile



    for item in data["results"]: # ищем нужный ключ в JSON-файле и проходим по всем его объектам

        #DisplayInformation in Tinder Profile
        disp_prof_inf = ET.SubElement(entity4, "DisplayInformation")
        label_profile = ET.SubElement(disp_prof_inf, "Label", Type="text/html")

        #объявляем все переменные, которые хранят нужные нам данные для поля DisplayInformation

        photo = data["results"][0]["photos"][0]["image"]
        name = XMLS.escape(str(item["name"])) #экранируем символ > в имени пользователя
        alias = item["alias"]
        description = item["description"]
        gender = item["gender"]
        if gender == "m":
            gender = "Male"
        else: gender = "Female"
        age = item["age"]
        city = item["city"]
        interests = ", ".join(item["interests"])
        work1 = item["jobs"][0]["position"]
        work2 = item["jobs"][0]["name"]
        education = item["educations"][0]
        spotify_theme = item["spotify_theme"]["name"]
        spotify_url = item["spotify_theme"]["preview_url"]


        label_profile.text = f'<![CDATA[<html> <img src="{photo}"height="150"/<br> <br> <b>Name:</b> {name} ' \
                                 f'| <a href="https://tinder.com/@{alias}">View Profile</a><br>' \
                                 f'<b>Description:</b> {description} <br> <b>Gender:</b> {gender}' \
                                 f'<br> <b>Age:</b> {age}<br> <b>City:</b> {city}<br>' \
                                 f'<b>Interests:</b> {interests}<br> <b>Work:</b> {work1} at {work2}<br>' \
                                 f'<b>Education:</b> {education}<br> <b>Spotify Theme:</b> {spotify_theme}' \
                             f'| <a href={spotify_url}>Preview Link</a><br></html>]]>'\
                .format(photo=str(photo), name = name, alias = alias, description = description,
                        gender = gender, age = age, city = city, interests = interests, work1 = work1, work2 = work2,
                        education = education, spotify_theme = spotify_theme, spotify_url = spotify_url)



        # Entity Location
        if "city" in item:
            # Создаем новый элемент XML для города и добавляем его значение в атрибут
            city_elem = ET.SubElement(entity1, "Field", DisplayName="City")
            city_elem.text = item["city"]
            # Добавляем элемент "value" внутри элемента "Field"
            value_elem = ET.SubElement(entity1, "Value")
            value_elem.text = item["city"]

        # Entity Company jobs
        if "jobs" in item:
            for job in item["jobs"]: #тут цикл так как в jobs много пар ключ-значение
                if "name" in job:
                    field = ET.SubElement(entity2, "Field", DisplayName="Name")
                    field.text = job["name"]
                    value_elem = ET.SubElement(entity2, "Value")
                    value_elem.text = job["name"]
                    display_information = ET.SubElement(entity2, "DisplayInformation")
                    label = ET.SubElement(display_information, "Label", Type="text/html")
                    label.text = "<![CDATA[<html><b>Name: </b>{ja}<br></html>]]>".format(ja=job["name"])

        # Entity Company educations
        if "educations" in item: #тут цикла for не будет, так как пара ключ-значение всего одна
            education_array = data["results"][0]["educations"][0]
            field = ET.SubElement(entity3, "Field", DisplayName="Name")
            field.text = str(education_array)
            value_elem = ET.SubElement(entity3, "Value")
            value_elem.text = str(education_array)
            display_information = ET.SubElement(entity3, "DisplayInformation")
            label = ET.SubElement(display_information, "Label", Type="text/html")
            label.text = "<![CDATA[<html><b>Name: </b>{education_array}<br></html>]]>"\
                .format(education_array = education_array)


        # Tinder Profile
        if "id" in item:
            id_elem = ET.SubElement(entity4, "Value")
            id_elem.text = item["id"]

        # Image
        if "photos" in item:
            photo = data["results"][0]["photos"][0]["image"]
            user_photo = ET.SubElement(entity4, "Image")
            user_photo.text = str(photo)

        #Fields of Tinder Profile
        if "name" in item:
            user_name = ET.SubElement(fields_for_profile, "Field", DisplayName="Name")
            user_name.text = XMLS.escape(str(item["name"]))
        if "alias" in item:
            user_url = ET.SubElement(fields_for_profile, "Field", DisplayName="URL")
            user_url.text = "https://tinder.com/@{alias}".format(alias=item["alias"])
            user_alias = ET.SubElement(fields_for_profile, "Field", DisplayName="Alias")
            user_alias.text = item["alias"]
        if "description" in item:
            user_desc = ET.SubElement(fields_for_profile, "Field", DisplayName="Description")
            user_desc.text = item["description"]
        if "gender" in item:
            user_gender = ET.SubElement(fields_for_profile, "Field", DisplayName="Gender")
            if item["gender"] == "m":
                user_gender.text = "Male"
            else: user_gender.text = "Female"
        if "city" in item:
            user_city = ET.SubElement(fields_for_profile, "Field", DisplayName="City")
            user_city.text = item["city"]
        if "interests" in item:
            interests_str = ", ".join(item["interests"])
            user_interests = ET.SubElement(fields_for_profile, "Field", DisplayName="Interests")
            user_interests.text = interests_str
        if "jobs" in item:
            for job in item["jobs"]:
                if "name" and "position" in job:
                    user_work = ET.SubElement(fields_for_profile, "Field", DisplayName="Work")
                    user_work.text = job["position"] + ' at ' + job["name"]
        if "spotify_theme" in item:
                if "name" in item["spotify_theme"]:
                    user_sptheme = ET.SubElement(fields_for_profile, "Field", DisplayName="Spotify Theme")
                    user_sptheme.text = item["spotify_theme"]["name"]
        if "educations" in item:
            education_array = data['results'][0]['educations'][0]
            user_education = ET.SubElement(fields_for_profile, "Field", DisplayName="Education")
            user_education.text = str(education_array)
        if "spotify_theme" in item:
                if "preview_url" in item["spotify_theme"]:
                    user_spthemeurl = ET.SubElement(fields_for_profile, "Field", DisplayName="Spotify Theme URL")
                    user_spthemeurl.text = item["spotify_theme"]["preview_url"]




    #Записываем все в XML-файл
    xml_file_path = json_file_path.replace(".json", ".xml")
    with open(xml_file_path, "w", encoding="utf-8") as xml_file:
        xml_file.write(ET.tostring(root, encoding="unicode"))


#Вызов функции
convert_json_to_xml("C:\PythonProjects\SL_JSON_2_XML\example.json")
