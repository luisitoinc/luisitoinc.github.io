import pandas as pd
import seaborn as sns
import altair as alt
import matplotlib.pyplot as plt
import numpy as np
import forms



from flask import Flask
from flask import request 
from flask import render_template
from flask import make_response
from flask import session 
from flask_wtf import CsrfProtect 
from flask import url_for
from flask import redirect


app = Flask(__name__)
app.secret_key="my_secret_key"
csrf = CsrfProtect(app)



#Cargamos el archivo csv 
##data = pd.read_csv("Titulados_Educacion_Superior_2019.csv",sep=";",low_memory=False)
data=pd.read_csv("export_dataframe .csv")
#dt contiene toda nuestra base de datos de titulados 2019
dt=pd.DataFrame(data)


#Utilizamos como filtro el nombre de la carrera (Informática) y creamos un DataFRame con estos datos generando dtInf
##dt['NOMB_CARRERA']=dt['NOMB_CARRERA'].str.lower()
##dtInf = pd.DataFrame(dt[dt['NOMB_CARRERA'].str.contains('informatic')])

dtInf = dt       

##dtInf.to_csv (r'C:\Users\Luis\Desktop\export_dataframe .csv', index = False)

dtInfi = pd . Series (dtInf["NOMB_INST"].value_counts().head(3))
dtt1 = pd.DataFrame(dtInf[dtInf['NOMB_INST'].str.contains(dtInfi.index[0])])
dtt2 = pd.DataFrame(dtInf[dtInf['NOMB_INST'].str.contains(dtInfi.index[1])])
dtt3 = pd.DataFrame(dtInf[dtInf['NOMB_INST'].str.contains(dtInfi.index[2])])


@app.route("/", methods = ["GET","POST"])
def index():
    #custome_cookie = request.cookies.get("custome_cookies")
    #print(custome_cookie)
    #comment_form = forms.CommentForm(request.form)

    if "Region"  in session:
        Region = session["Region"]
        print(Region)
        #print(comment_form.Region.data)
        #print(comment_form.email.data)
        #print(comment_form.comment.data)

    title="index"
    
    return render_template("index.html",  title=title)




@app.route("/principal", methods = ["GET","POST"])
def principal():
    
    login_form = forms.LoginForm(request.form)

    if request.method == "POST":
      session["Region"] = login_form.Region.data



    enlaces=[{"url":"http://127.0.0.1:5000/grafico2","texto":"Grafico interactivo Relación alumnos titulados - Sede - Tipo Jornada"},
			{"url":"http://127.0.0.1:5000/grafico3","texto":"N° Titulados por institución"},
			{"url":"http://127.0.0.1:5000/grafico5","texto":"DUOC UC"},
            {"url":"http://127.0.0.1:5000/grafico6","texto":"INACAP"},
            {"url":"http://127.0.0.1:5000/grafico7","texto":"AIEP"},
            {"url":"http://127.0.0.1:5000/grafico8","texto":"TÍTULO OBTENIDO REGIÓN METROPOLITANA"},
            {"url":"http://127.0.0.1:5000/grafico9","texto":"TÍTULO SEGÚN REGIÓN"},
			]


    return render_template("login.html",  form =login_form , enlaces=enlaces)



    


@app.route("/cookie")
def cookie():
    response = make_response(  render_template("cookie.html")     )
    response.set_cookie("custome_cookie","LUIS")
   
    
    return response




@app.route("/grafico2/")
def grafico2():
    
    dtInf.EDAD_ALU = dtInf.EDAD_ALU.astype(int)

    tabla = alt.Chart(dtInf).mark_circle().encode(
    alt.X('EDAD_ALU', axis=alt.Axis(title='EDAD DEL ALUMNO')),
    alt.Y('NOMB_SEDE', axis=alt.Axis(title='SEDE')),
    color='JORNADA'
    ).interactive()

    return  tabla.to_html()



@app.route("/grafico3/")
def grafico3():
    
    tabla3 = alt.Chart(dtInf).mark_bar().encode(
    alt.X('NOMB_INST', axis=alt.Axis(title='INSTITUCIÓN')),
    alt.Y('count()',axis=alt.Axis(title='N° TITULADOS'))
    ).interactive()

    return  tabla3.to_html()

@app.route("/grafico5/")
def grafico5():
    
    tabla5= alt.Chart(dtt1).mark_bar().encode(
    alt.Y('REGION_SEDE', axis=alt.Axis(title='REGION')),
    alt.X('count()',axis=alt.Axis(title='N° TITULADOS')),
    color="NOMB_INST"
    ).interactive()
        
        
    return  tabla5.to_html()


@app.route("/grafico6/")
def grafico6():
    
    tabla6= alt.Chart(dtt2).mark_bar().encode(
    alt.Y('REGION_SEDE', axis=alt.Axis(title='REGION')),
    alt.X('count()',axis=alt.Axis(title='N° TITULADOS')),
    color="NOMB_INST"
    ).interactive()
        
    return  tabla6.to_html()


@app.route("/grafico7/")
def grafico7():
    
    tabla7=alt.Chart(dtt3).mark_bar().encode(
    alt.Y('REGION_SEDE', axis=alt.Axis(title='REGION')),
    alt.X('count()',axis=alt.Axis(title='N° TITULADOS')),
    color="NOMB_INST"
    ).interactive()
        
    return  tabla7.to_html()

@app.route("/grafico8/")
def grafico8():
    
    dtMetropolitana = pd.concat([dtt1,dtt2,dtt3])

    dtMetropolitana


    tabla8=alt.Chart(dtMetropolitana).mark_bar().encode(
    alt.Y('NOMB_TITULO_OBTENIDO', axis=alt.Axis(title='TÍTULO OBTENIDO')),
    alt.X('count()',axis=alt.Axis(title='N° TITULADOS')),
    color = "NOMB_INST"
    ).interactive()
        
    return  tabla8.to_html()



@app.route("/grafico9/")
def grafico9():
    
    dtt4 = pd.DataFrame(dtInf[dtInf['REGION_SEDE'].str.contains(session["Region"])])

    tabla9 = alt.Chart(dtt4).mark_bar().encode(
    alt.Y('NOMB_INST', axis=alt.Axis(title='INSTITUCIONES')),
    alt.X('count()',axis=alt.Axis(title='N° TITULADOS')),
    color="NOMB_INST"
    ).interactive()


    if "Region" in session:
      
        session.pop("Region")
        
    return  tabla9.to_html()

@app.route('/enlaces')
def enlaces():
	enlaces=[{"url":"http://127.0.0.1:5000/grafico2","texto":"Grafico interactivo Relación alumnos titulados - Sede - Tipo Jornada"},
			{"url":"http://127.0.0.1:5000/grafico3","texto":"N° Titulados por institución"},
			{"url":"http://127.0.0.1:5000/grafico5","texto":"DUOC UC"},
            {"url":"http://127.0.0.1:5000/grafico6","texto":"INACAP"},
            {"url":"http://127.0.0.1:5000/grafico7","texto":"AIEP"},
            {"url":"http://127.0.0.1:5000/grafico8","texto":"TÍTULO OBTENIDO REGIÓN METROPOLITANA"},
            {"url":"http://127.0.0.1:5000/grafico9","texto":"TÍTULO SEGÚN REGIÓN"},
			]
	return render_template("template4.html",enlaces=enlaces)



@app.route("/logout")
def logout():
    if "Region" in session:
      
        session.pop("Region")
    return redirect(url_for("grafico"))


if __name__ == "__main__":
    app.run(debug = True)