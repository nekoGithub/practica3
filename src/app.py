from flask import Flask, request, render_template, redirect, url_for, session
app = Flask(__name__)
app.secret_key = 'unaclavesecreta'

def generar_id():
    if 'seminarios' in session and len(session['seminarios']) > 0:
        return max(item['id'] for item in session['seminarios' ]) + 1
    else:
        return 1

@app.route('/')
def index():
    if 'seminarios' not in session:
        session['seminarios'] = []
    
    seminarios = session.get('seminarios',[])
    return render_template('index.html', seminarios=seminarios)


@app.route('/nuevo', methods=['POST','GET'])
def nuevo():
    seminarios = [
        'Inteligencia Artificial',
        'Machine Learning',
        'Simulacion con arena',
        'Robotica Educativa'
    ]
    if request.method == 'POST':
        fecha = request.form['fecha']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        turno = request.form['turno']
        seminarios_seleccionados  = request.form.getlist('seminarios[]')

        nuevoSeminario = {
            'id': generar_id(),
            'fecha': fecha,
            'nombre': nombre,
            'apellido': apellido,
            'turno': turno,
            'seminarios': seminarios_seleccionados,
            
        }

        if 'seminarios' not in session:
            session['seminarios'] = []

        session['seminarios'].append(nuevoSeminario)
        session.modified = True
        return redirect(url_for('index'))
    
    return render_template('nuevo.html',seminarios=seminarios)

@app.route('/editar/<int:id>', methods=['POST','GET'])
def editar(id):
    listaSeminariosInscritos = session.get('seminarios',[])
    seminario = next((c for c in listaSeminariosInscritos if c['id'] == id), None)
    if not seminario:
        return redirect(url_for('index'))
    
    lista_seminarios_disponibles = [
        'Inteligencia Artificial',
        'Machine Learning',
        'Simulacion con arena',
        'Robotica Educativa'
    ]

    if request.method == 'POST':
        
        seminario['fecha'] = request.form['fecha']
        seminario['nombre'] = request.form['nombre']
        seminario['apellido'] = request.form['apellido']
        seminario['turno'] = request.form['turno']
        seminario['seminarios'] = request.form.getlist('seminarios[]')  
          
        session.modified = True

        for index, item in enumerate(listaSeminariosInscritos):
            if item['id'] == id:
                listaSeminariosInscritos[index] = seminario
                break
        session['seminarios'] = listaSeminariosInscritos
        return redirect(url_for('index'))
    return render_template('editar.html', seminario=seminario, lista_seminarios_disponibles =lista_seminarios_disponibles)

@app.route('/eliminar/<int:id>', methods=['POST','GET'])
def eliminar(id):
    listaSeminariosInscritos = session.get('seminarios', [])
    seminario = next((c for c in listaSeminariosInscritos if c['id'] == id), None)
    if seminario:
        session['seminarios'].remove(seminario)
        session.modified = True
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)