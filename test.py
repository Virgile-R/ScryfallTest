from yattag import Doc
import math
import json
import imgkit
import requests
import os.path
from os import path
def generate_monster_block(monster):
   
    monster = "-".join(monster).lower()
    apiurl = "https://www.dnd5eapi.co/api/monsters/"+ monster
    data = requests.get(apiurl).json()


    output = f"./img/{monster}.png"
    if path.exists(f'./img/{monster}.png'):
        return output
    else: 
        doc, tag, text = Doc().tagtext()
        doc.asis('<!DOCTYPE html><link rel="stylesheet" href="..\css\stylednd.css"> <link href="https://fonts.googleapis.com/css?family=Libre+Baskerville:7monstermonster" rel="stylesheet" type="text/css">', '<link href="https://fonts.googleapis.com/css?family=Noto+Sans:4monstermonster,7monstermonster,4monstermonsteritalic,7monstermonsteritalic" rel="stylesheet" type="text/css">', '<div class="stat-block wide">	<hr class="orange-border" /> <div class="section-left"> <div class="creature-heading">')

        with tag('h1'):
            text(data['name'])
        with tag('h2'):
            text(data['size'] + " " + data['type'] + " " + data['alignment'])
        doc.asis("""</div> <!-- creature heading -->
                <svg height="5" width="100%" class="tapered-rule">
                <polyline points="0,0 400,2.5 0,5"></polyline>
            </svg>
                <div class="top-stats">
                    <div class="property-line first">
                        <h4>Armor Class</h4>: """)
        with tag('p'):
            text(data['armor_class'])
        doc.asis("""</div> <!-- property line -->
                    <div class="property-line">
                        <h4>Hit Points</h4>: """)
        with tag('p'):
            text(data['hit_points'])
        doc.asis("""</div> <!-- property line -->
                    <div class="property-line last">
                        <h4>Speed</h4>: """) 
        with tag('p'):
            for i in data['speed']:
                
                text(i + ":" + data['speed'][i])  
        doc.asis("""</div> <!-- property line -->
                    <svg height="5" width="100%" class="tapered-rule">
                <polyline points="0,0 400,2.5 0,5"></polyline>
            </svg>
                    <div class="abilities">
                        <div class="ability-strength">
                            <h4>STR</h4>""")
        with tag('p'):
            ab= data['strength']
            ab_mod= (data['strength'] - 10)/2
            if ab_mod >= 0:
                text(f"{ab} (+{math.floor(ab_mod)})" )
            else:
                text(f"{ab} (  {math.floor(ab_mod)})" )
        doc.asis("""</div> <!-- ability strength -->
                        <div class="ability-dexterity">
                            <h4>DEX</h4>""")
        with tag('p'):
            ab= data['dexterity']
            ab_mod= (ab - 10)/2
            if ab_mod >= 0:
                text(f"{ab} (+{math.floor(ab_mod)})" )
            else:
                text(f"{ab} (  {math.floor(ab_mod)})" )
        doc.asis("""</div> <!-- ability dexteriry -->
                        <div class="ability-constitution">
                            <h4>CON</h4>""")                
        with tag('p'):
            ab= data['constitution']
            ab_mod= (ab - 10)/2
            if ab_mod >= 0:
                text(f"{ab} (+{math.floor(ab_mod)})" )
            else:
                text(f"{ab} (  {math.floor(ab_mod)})" )
        doc.asis("""</div> <!-- ability constitution -->
                        <div class="ability-intelligence">
                            <h4>INT</h4>""")
        with tag('p'):
            ab= data['intelligence']
            ab_mod= (ab - 10)/2
            if ab_mod >= 0:
                text(f"{ab} (+{math.floor(ab_mod)})" )
            else:
                text(f"{ab} (  {math.floor(ab_mod)})" )
        doc.asis("""</div> <!-- ability intelligence -->
                        <div class="ability-wisdom">
                            <h4>WIS</h4>""")
        with tag('p'):
            ab= data['wisdom']
            ab_mod= (ab - 10)/2
            if ab_mod >= 0:
                text(f"{ab} (+{math.floor(ab_mod)})" )
            else:
                text(f"{ab} (  {math.floor(ab_mod)})" )
        doc.asis("""</div> <!-- ability wisdom -->
                        <div class="ability-charisma">
                            <h4>CHA</h4>""")
        with tag('p'):
            ab= data['charisma']
            ab_mod= (ab - 10)/2
            if ab_mod >= 0:
                text(f"{ab} (+{math.floor(ab_mod)})" )
            else:
                text(f"{ab} (  {math.floor(ab_mod)})" )                   
        doc.asis("""</div> <!-- ability charisma --> </div> <!-- abilities -->
                    <svg height="5" width="100%" class="tapered-rule">
                <polyline points="0,0 400,2.5 0,5"></polyline>
            </svg>
                    <div class="property-line first">
                        <h4>Damage Immunities</h4>: """)
        with tag('p'):
            if data['damage_immunities']:
                text(data['damage_immunities'] )
            else:
                text("None")
        doc.asis("""</div> <!-- property line -->
                    <div class="property-line">
                        <h4>Condition Immunities</h4>: """)
        with tag('p'):
            if data['condition_immunities']:
                text(data['damage_immunities'] )
            else:
                text("None")
        doc.asis("""</div> <!-- property line -->
                    <div class="property-line">
                        <h4>Senses</h4>: """)
        with tag('p'):
            for a in data['senses']:
                text(data['senses'][a])  
        doc.asis("""</div> <!-- property line -->
                    <div class="property-line">
                        <h4>Languages</h4>: """)
        with tag('p'):
            text(data['languages'])  
        doc.asis("""</div> <!-- property line -->
                    <div class="property-line last">
                        <h4>Challenge</h4>: """)
        with tag('p'):
            text(data['challenge_rating'] )
        doc.asis("""</div> <!-- property line -->
                </div> <!-- top stats -->
                <svg height="5" width="100%" class="tapered-rule">
                <polyline points="0,0, 400,2.5 0,5"></polyline>
            </svg>
                <div class="property-block">  """)
        if 'special_abilities' in data:
            with tag('p'):
                special_ability = [ (i['name'], i['desc']) for i in data['special_abilities']]
                for i, a in enumerate(special_ability):
                    doc.asis(f"<span class=\"br\"><b> {a[0]}</b> : {a[1]}</span></br>" ) 
            doc.asis("""</div> <!-- property block-->
                </div> <!-- section left -->
                <div class="section-right">
                    <div class="actions">
                        <h3>Actions</h3>
                        <div class="property-block"> """)
        with tag('p'):
            actions = [ (i['name'], i['desc']) for i in data['actions']]
            for i, a in enumerate(actions):
                doc.asis(f"<span class=\"br\"><b> {a[0]}</b> : {a[1]}</span></br>" )
        doc.asis("""</div> <!-- property block -->
                    
                </div> <!-- actions -->
        """   )     
        if 'legendary_actions' in data:
            doc.asis("""<div class="actions">
                    <h3>Legendary Actions</h3>
                    <div class="property-block">
                        """)
            with tag('p'):
                legactions = [ (i['name'], i['desc']) for i in data['legendary_actions']]
                for i, a in enumerate(legactions):
                    doc.asis(f"<span class=\"br\"><b> {a[0]}</b> : {a[1]}</span></br>" )
            doc.asis("""</div> <!-- property block -->
                    
                    
                </div> <!-- actions -->
            </div> <!-- section right -->
            <hr class="orange-border bottom" />
        </div> <!-- stat block -->
        """)     


        content = doc.getvalue()

        with open('./html/test.html', 'w', encoding='UTF8') as test_file:
            test_file.write(content)

        options= {
            'enable-local-file-access': '',
            'width': '1920',
            
        }


        imgkit.from_file("./html/test.html", output, options=options)
        
        return output