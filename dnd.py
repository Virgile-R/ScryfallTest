from yattag import Doc
import math
import json
import imgkit
import requests
import os.path
from os import path
import boto3

imgkitconfig = imgkit.config(wkhtmltoimage="/app/bin/wkhtmltoimage")
s3 = boto3.resource('s3')
class Monster:
    def __init__(self, monster) -> None:
        apiurl = "https://www.dnd5eapi.co/api/monsters/"+ monster
         
        r = requests.get(apiurl)
        if r.status_code == 404:
            raise ValueError
        else:
            data = r.json()

            self.index = data['index']
            self.name = data['name']
            self.size = data['size']
            self.type = data['type']
            self.subtype = data['subtype']
            self.alignment = data['alignment']
            self.ac = data['armor_class']
            self.hp = data['hit_points']
            self.hd = data['hit_dice']
            if 'forms' in data: 
                self.forms = data['forms']
            self.speed = data['speed']
            self.str = data['strength']
            self.dex = data['dexterity']
            self.con = data['constitution']
            self.int = data['intelligence']
            self.wis = data['wisdom']
            self.cha = data['charisma']
            if 'profiences' in data:
                self.prof = data['profiencies']
            if 'damage_vulnerabilities' in data:
                self.dv = data['damage_vulnerabilities']
            if 'damage_resistances' in data:
                self.dr = data['damage_resistances']
            if 'damage_immunities' in data:
                self.di = data['damage_immunities']
            if 'condition_immunities' in data:
                self.ci = data['condition_immunities']
            self.senses = data['senses']
            self.lang = data['languages']
            self.cr = data['challenge_rating']
            if 'special_abilities' in data:
                self.sa = data['special_abilities']
            self.action = data['actions']
            if 'legendary_actions' in data:
                self.legact = data['legendary_actions']
            self.url = data['url']




 
    


def generate_monster_block(m):
    output = f"./img/{m.index}.jpg"
    if path.exists(f'./img/{m.index}.jpg'):
        return output
    else: 
        doc, tag, text = Doc().tagtext()
        doc.asis('<!DOCTYPE html><link rel="stylesheet" href="..\css\stylednd.css"> <link href="http://fonts.googleapis.com/css?family=Libre+Baskerville:7monstermonster" rel="stylesheet" type="text/css">', '<link href="http://fonts.googleapis.com/css?family=Noto+Sans:4monstermonster,7monstermonster,4monstermonsteritalic,7monstermonsteritalic" rel="stylesheet" type="text/css">', '<div class="stat-block wide">	<hr class="orange-border" /> <div class="section-left"> <div class="creature-heading">')

        with tag('h1'):
            text(m.name)
        with tag('h2'):
            text(m.size + " " + m.type + " " + m.alignment)
        doc.asis("""</div> <!-- creature heading -->
                <svg height="5" width="100%" class="taperedrule">
                <polyline points="0,0 400,2.5 0,5"></polyline>
            </svg>
                <div class="top-stats">
                    <div class="property-line first">
                        <h4>Armor Class</h4>: """)
        with tag('p'):
            text(m.ac)
        doc.asis("""</div> <!-- property line -->
                    <div class="property-line">
                        <h4>Hit Points</h4>: """)
        with tag('p'):
            text(m.hp)
        doc.asis("""</div> <!-- property line -->
                    <div class="property-line last">
                        <h4>Speed</h4>: """) 
        with tag('p'):
            for i in m.speed:
                
                text(i + ":" + m.speed[i])  
        doc.asis("""</div> <!-- property line -->
                    <svg height="5" width="100%" class="taperedrule">
                <polyline points="0,0 400,2.5 0,5"></polyline>
            </svg>
                    <div class="abilities">
                        <div class="ability-strength">
                            <h4>STR</h4>""")
        with tag('p'):
            ab= m.str
            ab_mod= (m.str - 10)/2
            if ab_mod >= 0:
                text(f"{ab} (+{math.floor(ab_mod)})" )
            else:
                text(f"{ab} (  {math.floor(ab_mod)})" )
        doc.asis("""</div> <!-- ability strength -->
                        <div class="ability-dexterity">
                            <h4>DEX</h4>""")
        with tag('p'):
            ab= m.dex
            ab_mod= (ab - 10)/2
            if ab_mod >= 0:
                text(f"{ab} (+{math.floor(ab_mod)})" )
            else:
                text(f"{ab} (  {math.floor(ab_mod)})" )
        doc.asis("""</div> <!-- ability dexteriry -->
                        <div class="ability-constitution">
                            <h4>CON</h4>""")                
        with tag('p'):
            ab= m.con
            ab_mod= (ab - 10)/2
            if ab_mod >= 0:
                text(f"{ab} (+{math.floor(ab_mod)})" )
            else:
                text(f"{ab} (  {math.floor(ab_mod)})" )
        doc.asis("""</div> <!-- ability constitution -->
                        <div class="ability-intelligence">
                            <h4>INT</h4>""")
        with tag('p'):
            ab= m.int
            ab_mod= (ab - 10)/2
            if ab_mod >= 0:
                text(f"{ab} (+{math.floor(ab_mod)})" )
            else:
                text(f"{ab} (  {math.floor(ab_mod)})" )
        doc.asis("""</div> <!-- ability intelligence -->
                        <div class="ability-wisdom">
                            <h4>WIS</h4>""")
        with tag('p'):
            ab= m.wis
            ab_mod= (ab - 10)/2
            if ab_mod >= 0:
                text(f"{ab} (+{math.floor(ab_mod)})" )
            else:
                text(f"{ab} (  {math.floor(ab_mod)})" )
        doc.asis("""</div> <!-- ability wisdom -->
                        <div class="ability-charisma">
                            <h4>CHA</h4>""")
        with tag('p'):
            ab= m.cha
            ab_mod= (ab - 10)/2
            if ab_mod >= 0:
                text(f"{ab} (+{math.floor(ab_mod)})" )
            else:
                text(f"{ab} (  {math.floor(ab_mod)})" )                   
        doc.asis("""</div> <!-- ability charisma --> </div> <!-- abilities -->
                    <svg height="5" width="100%" class="taperedrule">
                <polyline points="0,0 400,2.5 0,5"></polyline>
            </svg>
                    <div class="property-line first">
                        <h4>Damage Immunities</h4>: """)
        with tag('p'):
            try:
                for i in m.di:
                    text(f"{i}, ") 
            except AttributeError:
                text("None")
        
        doc.asis("""</div> <!-- property line -->
                    <div class="property-line">
                        <h4>Condition Immunities</h4>: """)
        with tag('p'):
            try :
                for i in m.ci:
                    text(f'{i}, ' ) 
            except AttributeError:
                text("None")
        doc.asis("""</div> <!-- property line -->
                    <div class="property-line">
                        <h4>Senses</h4>: """)
        with tag('p'):
            for a in m.senses:
                text(m.senses[a])  
        doc.asis("""</div> <!-- property line -->
                    <div class="property-line">
                        <h4>Languages</h4>: """)
        with tag('p'):
            text(m.lang)  
        doc.asis("""</div> <!-- property line -->
                    <div class="property-line last">
                        <h4>Challenge</h4>: """)
        with tag('p'):
            text(m.cr)
        doc.asis("""</div> <!-- property line -->
                </div> <!-- top stats -->
                <svg height="5" width="100%" class="taperedrule">
                <polyline points="0,0, 400,2.5 0,5"></polyline>
            </svg>
                <div class="property-block">  """)
        try:
            with tag('p'):
                special_ability = [ (i['name'], i['desc']) for i in m.sa]
                for i, a in enumerate(special_ability):
                    doc.asis(f"<span class=\"br\"><b> {a[0]}</b> : {a[1]}</span></br>" ) 
            doc.asis("""</div> <!-- property block-->
                </div> <!-- section left -->
                <div class="sectionright">
                    <div class="actions">
                        <h3>Actions</h3>
                        <div class="property-block"> """)
        except AttributeError:
            pass
        with tag('p'):
            actions = [ (i['name'], i['desc']) for i in m.action]
            for i, a in enumerate(actions):
                doc.asis(f"<span class=\"br\"><b> {a[0]}</b> : {a[1]}</span></br>" )
        doc.asis("""</div> <!-- property block -->
                    
                </div> <!-- actions -->
        """   )  
        

        ##try:
        if hasattr(m, 'legact'):
            doc.asis("""<div class="actions">
                    <h3>Legendary Actions</h3>
                    <div class="property-block">
                        """)
            with tag('p'):
                legactions = [ (i['name'], i['desc']) for i in m.legact]
                for i, a in enumerate(legactions):
                    doc.asis(f"<span class=\"br\"><b> {a[0]}</b> : {a[1]}</span></br>" )
            doc.asis("""</div> <!-- property block -->
                    
                    
                </div> <!-- actions -->
            </div> <!-- section right -->
            <hr class="orange-border bottom" />
        </div> <!-- stat block -->
        """)
        # except AttributeError:
        #     pass


        content = doc.getvalue()

        with open(f'./html/{m.index}.html', 'w+', encoding='UTF8') as test_file:
            test_file.write(content)
        file = open(f'./html/{m.index}.html', 'rb')
        s3.Bucket('scryfall-assets').put_object(Key=f'/html/{m.index}.html', Body=file)
        options= {
            'enable-local-file-access': '',
            'width': '1280',
            'quality': 50
            
            
        }

        awsurl = 'https://scryfall-assets.s3.eu-west-3.amazonaws.com//html/'+ m.index+'.html'
        print(awsurl)
        imgkit.from_url(awsurl, output, config=imgkitconfig, options=options)
        
        return output
