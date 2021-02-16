import fitz
import pandas

doc = fitz.open('output/A06303.pdf') # Archivo origen
padron = []

for page in doc:
    print("Parsing Page " + str(page.number) + "/" + str(len(doc)))
    
    dic = page.getText("dict")

    # Campos están antecedidos por un dos puntos y espacio
    # ": DEL LIBERTADOR GENERAL BERNARDO O'HIGGINS"
    region = dic['blocks'][153]['lines'][1]['spans'][0]['text'][2:]
    provincia = dic['blocks'][154]['lines'][1]['spans'][0]['text'][2:]
    comuna = dic['blocks'][155]['lines'][1]['spans'][0]['text'][2:]

    # print(region, provincia, comuna)


    # Antes del bloque 156 se repite marca de agua SERVEL
    for block in dic['blocks'][157:]:
        # dependiendo de cuantas lineas tiene el bloque (parrafo) es como se interpreta el orden de los campos
        if len(block['lines']) == 6:
            nombre = block['lines'][0]['spans'][0]['text']
            ci = block['lines'][1]['spans'][0]['text']
            genero_direccion = block['lines'][2]['spans'][0]['text']
            gd_index = genero_direccion.find(' ')
            genero = genero_direccion[:gd_index]
            direccion = genero_direccion[gd_index+1:]
            circunscripcion = block['lines'][3]['spans'][0]['text']
            mesa = block['lines'][4]['spans'][0]['text']
            pueblo_indigena = block['lines'][5]['spans'][0]['text']

        else:
            nombre = block['lines'][0]['spans'][0]['text']
            ci = block['lines'][1]['spans'][0]['text']
            # ej: ' CONVENTO VIEJO 171 CALLE CONVENTO VIEJO CALLE CONVENTO VIEJO 171 CHIMBARONGO'
            genero_direccion = block['lines'][2]['spans'][0]['text']
            genero_index = genero_direccion.find(' ')
            genero = genero_direccion[:genero_index]
            direccion = genero_direccion[genero_index+1:]
            circunscripcion = block['lines'][3]['spans'][0]['text']
            mesa = block['lines'][4]['spans'][0]['text']
            pueblo_indigena = ""
        #print(nombre, ci, genero, direccion, circunscripcion, mesa, sep=',')

        padron.append({
            'Nombre': nombre,
            'CI': ci,
            'Genero': genero,
            'Direccion': direccion,
            'Circunscripcion': circunscripcion,
            'Mesa': mesa,
            'Region': region,
            'Provincia': provincia,
            'Comuna': comuna
            'Pueblo Indigena': pueblo_indigena
        })
        
    #print('End page')

padron_df = pandas.DataFrame(padron)
padron_df.to_csv('./output_csv/A06303.csv', index=False) # CSV resultante

print('End')
