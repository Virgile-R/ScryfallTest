from yattag import Doc
import json
import imgkit
import requests

class DndMonster():
	def __init__(self, monster):
		apiurl = "https://www.dnd5eapi.co/api/monsters/"+ monster.lower
		self.data = requests.get(apiurl).json()
	#with open('html\srd_5e_monsters.json', 'r' ) as f:
	#	data = json.load(f)
		
	def generate_monster_image(data,):
		doc, tag, text = Doc().tagtext()
		doc.asis('<!DOCTYPE html><link rel="stylesheet" href="..\css\stylednd.css"> <link href="https://fonts.googleapis.com/css?family=Libre+Baskerville:700" rel="stylesheet" type="text/css">', '<link href="https://fonts.googleapis.com/css?family=Noto+Sans:400,700,400italic,700italic" rel="stylesheet" type="text/css">', '<div class="stat-block wide">	<hr class="orange-border" /> <div class="section-left"> <div class="creature-heading">')

		with tag('h1'):
			text(data[0]['name'])
		with tag('h2'):
			text(data[0]['meta'])
		doc.asis("""</div> <!-- creature heading -->
				<svg height="5" width="100%" class="tapered-rule">
				<polyline points="0,0 400,2.5 0,5"></polyline>
			</svg>
				<div class="top-stats">
					<div class="property-line first">
						<h4>Armor Class</h4>""")
		with tag('p'):
			text(data[0]['Armor Class'])
		doc.asis("""</div> <!-- property line -->
					<div class="property-line">
						<h4>Hit Points</h4>""")
		with tag('p'):
			text(data[0]['Hit Points'])
		doc.asis("""</div> <!-- property line -->
					<div class="property-line last">
						<h4>Speed</h4>""") 
		with tag('p'):
			text(data[0]['Speed'])  
		doc.asis("""</div> <!-- property line -->
					<svg height="5" width="100%" class="tapered-rule">
				<polyline points="0,0 400,2.5 0,5"></polyline>
			</svg>
					<div class="abilities">
						<div class="ability-strength">
							<h4>STR</h4>""")
		with tag('p'):
			text(data[0]['STR'], data[0]['STR_mod'] )
		doc.asis("""</div> <!-- ability strength -->
						<div class="ability-dexterity">
							<h4>DEX</h4>""")
		with tag('p'):
			text(data[0]['DEX'], data[0]['DEX_mod'] )
		doc.asis("""</div> <!-- ability dexteriry -->
						<div class="ability-constitution">
							<h4>CON</h4>""")                
		with tag('p'):
			text(data[0]['CON'], data[0]['CON_mod'] )
		doc.asis("""</div> <!-- ability constitution -->
						<div class="ability-intelligence">
							<h4>INT</h4>""")
		with tag('p'):
			text(data[0]['INT'], data[0]['INT_mod'] )  
		doc.asis("""</div> <!-- ability intelligence -->
						<div class="ability-wisdom">
							<h4>WIS</h4>""")
		with tag('p'):
			text(data[0]['WIS'], data[0]['WIS_mod'] ) 
		doc.asis("""</div> <!-- ability wisdom -->
						<div class="ability-charisma">
							<h4>CHA</h4>""")
		with tag('p'):
			text(data[0]['CHA'], data[0]['CHA_mod'] )                     
		doc.asis("""</div> <!-- ability charisma --> </div> <!-- abilities -->
					<svg height="5" width="100%" class="tapered-rule">
				<polyline points="0,0 400,2.5 0,5"></polyline>
			</svg>
					<div class="property-line first">
						<h4>Damage Immunities</h4>""")
		with tag('p'):
			text('None' )
		doc.asis("""</div> <!-- property line -->
					<div class="property-line">
						<h4>Condition Immunities</h4>""")
		with tag('p'):
			text('None')
		doc.asis("""</div> <!-- property line -->
					<div class="property-line">
						<h4>Senses</h4>""")
		with tag('p'):
			text(data[0]['Senses'] )
		doc.asis("""</div> <!-- property line -->
					<div class="property-line">
						<h4>Languages</h4>""")
		with tag('p'):
			text(data[0]['Languages'] )
		doc.asis("""</div> <!-- property line -->
					<div class="property-line last">
						<h4>Challenge</h4>""")
		with tag('p'):
			text(data[0]['Languages'] )
		doc.asis("""</div> <!-- property line -->
				</div> <!-- top stats -->
				<svg height="5" width="100%" class="tapered-rule">
				<polyline points="0,0 400,2.5 0,5"></polyline>
			</svg>
				<div class="property-block"> <h4>Traits</h4>""")
		with tag('p'):
			doc.asis(data[0]['Traits'] )
		doc.asis("""</div> <!-- property block -->
			</div> <!-- section left -->
			<div class="section-right">
				<div class="actions">
					<h3>Actions</h3>
					<div class="property-block"> <h4>Actions</h4>""")
		with tag('p'):
			doc.asis(data[0]['Actions'] )
		doc.asis("""</div> <!-- property block -->
					
				</div> <!-- actions -->
				<div class="actions">
					<h3>Legendary Actions</h3>
					<div class="property-block">
						<h4>Legendary Actions.</h4>""")
		with tag('p'):
			doc.asis(data[0]['Legendary Actions'] )
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
			'enable-local-file-access': ''
		}

		output = "./img/{monster}"
		imgkit.from_file("./html/test.html", "./img/output.png", options=options)
		




class DndTemplate:
    def __init__(self, model, css) -> None:
        pass



    def populate_template(model, css):
        pass

    