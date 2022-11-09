from wsgiref.validate import validator
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Prodserv, Products, Services, Admin
from . import db
from flask import Flask, render_template, request
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from googletrans import Translator
import nltk
import googletrans
import smtplib
import json
import numpy as np
nltk.download('all')
views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template("index.html")

@views.route('/formidentifier')
def formidentifier():
    return render_template("formidentifier.html")

@views.route('/prodform', methods=["GET", "POST"])
def prod():
    #all_prod = Products.query.all()

    translator = Translator()
    if request.method == "POST":
        prodcomment = request.form.get('prodcomment')
        trans = translator.translate(prodcomment, src="tl", dest="en")
        sid = SentimentIntensityAnalyzer()
        score = sid.polarity_scores(trans.text)
        compound = score['compound']
        prodtranscomment = trans.text
        if compound <= -0.1:
            
            custname = request.form.get('custname')
            custcontact = request.form.get('custcontact')
            custemail = request.form.get('custemail')
            custstatus = request.form.get('custstatus')
            branch = request.form.get('branch')
            prodpurchase = request.form.getlist('prodpurchase')
            product =",".join(map(str, prodpurchase))
            fb_variety = request.form.get('fb_variety')
            fb_presentation = request.form.get('fb_presentation')
            fb_quality = request.form.get('fb_quality')
            prodcomment = request.form.get('prodcomment')
            prodremark = "Negative"
 
            new_prodfb = Products(custname=custname, custcontact=custcontact, custemail=custemail, custstatus=custstatus, branch=branch, prodpurchase=product, fb_variety=fb_variety, fb_presentation=fb_presentation, fb_quality=fb_quality, prodcomment=prodcomment, prodtranscomment=prodtranscomment, prodremark=prodremark)
            new_prodservP = Prodserv(custname=custname, custcontact=custcontact, custemail=custemail, custstatus=custstatus, branch=branch, prodpurchase=product, fb_variety=fb_variety, fb_presentation=fb_presentation, fb_quality=fb_quality, prodcomment=prodcomment, prodtranscomment=prodtranscomment, prodremark=prodremark)
            db.session.add(new_prodfb)
            db.session.add(new_prodservP)
            db.session.commit()
            
            
            EMAIL_ADDRESS = 'wecarekumparessystem@gmail.com'
            EMAIL_PASSWORD = 'jryhawyjeijnidge'

            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()

                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                
                subject = 'NEGATIVE FEEDBACK ALERT!'
                body = f'Dear [Admin 1], \n A customer send a negative feedback about the product. Please review the feedback immediately. \n\n Feedback informations: \n {custname} \n {custcontact} \n {custemail} \n {custstatus} \n {branch} \n {prodpurchase} \n {fb_variety}\n {fb_presentation} \n {fb_quality} \n {prodcomment} \n {prodtranscomment} \n {prodremark}'


                msg = f'Subject: {subject}\n\n{body}'
                

                smtp.sendmail(EMAIL_ADDRESS, 'johnchristophersinamban@gmail.com', msg)
            flash('Product Feedback Added', category='success')
            
        elif compound >= 0.1:
            custname = request.form.get('custname')
            custcontact = request.form.get('custcontact')
            custemail = request.form.get('custemail')
            custstatus = request.form.get('custstatus')
            branch = request.form.get('branch')
            prodpurchase = request.form.getlist('prodpurchase')
            product =",".join(map(str, prodpurchase))
            fb_variety = request.form.get('fb_variety')
            fb_presentation = request.form.get('fb_presentation')
            fb_quality = request.form.get('fb_quality')
            prodcomment = request.form.get('prodcomment')
            prodremark = "Positive"
            
            new_prodfb = Products(custname=custname, custcontact=custcontact, custemail=custemail, custstatus=custstatus, branch=branch, prodpurchase=product, fb_variety=fb_variety, fb_presentation=fb_presentation, fb_quality=fb_quality, prodcomment=prodcomment, prodtranscomment=prodtranscomment, prodremark=prodremark)
            new_prodservP = Prodserv(custname=custname, custcontact=custcontact, custemail=custemail, custstatus=custstatus, branch=branch, prodpurchase=product, fb_variety=fb_variety, fb_presentation=fb_presentation, fb_quality=fb_quality, prodcomment=prodcomment, prodtranscomment=prodtranscomment, prodremark=prodremark)
            db.session.add(new_prodfb)
            db.session.add(new_prodservP)
            db.session.commit()
            flash('Product Feedback Added', category='success')
            
        else:
            custname = request.form.get('custname')
            custcontact = request.form.get('custcontact')
            custemail = request.form.get('custemail')
            custstatus = request.form.get('custstatus')
            branch = request.form.get('branch')
            prodpurchase = request.form.getlist('prodpurchase')
            product =",".join(map(str, prodpurchase))
            fb_variety = request.form.get('fb_variety')
            fb_presentation = request.form.get('fb_presentation')
            fb_quality = request.form.get('fb_quality')
            prodcomment = request.form.get('prodcomment')
            prodremark = "Neutral"
            
            new_prodfb = Products(custname=custname, custcontact=custcontact, custemail=custemail, custstatus=custstatus, branch=branch, prodpurchase=product, fb_variety=fb_variety, fb_presentation=fb_presentation, fb_quality=fb_quality, prodcomment=prodcomment, prodtranscomment=prodtranscomment, prodremark=prodremark)
            new_prodservP = Prodserv(custname=custname, custcontact=custcontact, custemail=custemail, custstatus=custstatus, branch=branch, prodpurchase=product, fb_variety=fb_variety, fb_presentation=fb_presentation, fb_quality=fb_quality, prodcomment=prodcomment, prodtranscomment=prodtranscomment, prodremark=prodremark)
            db.session.add(new_prodfb)
            db.session.add(new_prodservP)
            db.session.commit()
            flash('Product Feedback Added', category='success')
            return redirect(url_for('views.home'))

    prod = Products.query.all()       
    return render_template('prodform.html', prod = prod)


@views.route('/prodservform', methods=['GET', 'POST'])
def prodserv():
    
    translator =Translator()
    if request.method == 'POST':
        prodcomment = request.form.get('prodcomment')
        prodtrans = translator.translate(prodcomment, src="tl", dest="en")
        sid = SentimentIntensityAnalyzer()
        prodscore = sid.polarity_scores(prodtrans.text)
        prodcompound = prodscore['compound']
        prodtranscomment = prodtrans.text
        servcomment = request.form.get('servcomment')
        servtrans = translator.translate(servcomment, src="tl", dest="en")
        servscore = sid.polarity_scores(servtrans.text)
        servcompound = servscore['compound']
        servtranscomment = servtrans.text
        
        
        if prodcompound <= -0.1:
            if servcompound <= -0.1:
                custname = request.form.get('custname')
                custcontact = request.form.get('custcontact')
                custemail = request.form.get('custemail')
                custstatus = request.form.get('custstatus')
                branch = request.form.get('branch')
                prodpurchase = request.form.getlist('prodpurchase')
                product =",".join(map(str, prodpurchase))

                fb_variety = request.form.get('fb_variety')
                fb_presentation = request.form.get('fb_presentation')
                fb_quality = request.form.get('fb_quality')
                prodcomment = request.form.get('prodcomment')
                prodremark = "Negative"
        
                fb_empserv = request.form.get('fb_empserv')
                fb_speed = request.form.get('fb_speed')
                fb_clean = request.form.get('fb_clean')
                servcomment = request.form.get('servcomment')
                servremark = "Negative"
 
                new_servfb = Services(custname=custname, custcontact=custcontact, custemail=custemail, custstatus=custstatus, branch=branch, prodpurchase=product, fb_empserv=fb_empserv, fb_speed=fb_speed, fb_clean=fb_clean, servcomment=servcomment, servtranscomment=servtranscomment, servremark=servremark)
                new_prodservS = Prodserv(custname=custname, custcontact=custcontact, custemail=custemail, custstatus=custstatus, branch=branch, prodpurchase=product, fb_empserv=fb_empserv, fb_speed=fb_speed, fb_clean=fb_clean, servcomment=servcomment, servtranscomment=servtranscomment, servremark=servremark)                
                db.session.add(new_servfb)
                db.session.add(new_prodservS)

                new_prodfb = Products(custname=custname, custcontact=custcontact, custemail=custemail, custstatus=custstatus, branch=branch, prodpurchase=product, fb_variety=fb_variety, fb_presentation=fb_presentation, fb_quality=fb_quality, prodcomment=prodcomment, prodtranscomment=prodtranscomment, prodremark=prodremark)
                new_prodservP = Prodserv(custname=custname, custcontact=custcontact, custemail=custemail, custstatus=custstatus, branch=branch, prodpurchase=product, fb_variety=fb_variety, fb_presentation=fb_presentation, fb_quality=fb_quality, prodcomment=prodcomment, prodtranscomment=prodtranscomment, prodremark=prodremark)
                db.session.add(new_prodfb)
                db.session.add(new_prodservP)
                db.session.commit()
                
                EMAIL_ADDRESS = 'wecarekumparessystem@gmail.com'
                EMAIL_PASSWORD = 'jryhawyjeijnidge'

                with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                    smtp.ehlo()
                    smtp.starttls()
                    smtp.ehlo()

                    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                
                    subject = 'NEGATIVE FEEDBACK ALERT!'
                    body = f'Dear [Admin 1], \n A customer send a negative feedback about the product and service. Please review the feedback immediately. \n\n Feedback informations: \n {custname} \n {custcontact} \n {custemail} \n {custstatus} \n {branch} \n {prodpurchase} \n {fb_variety}\n {fb_presentation} \n {fb_quality} \n {prodcomment} \n {prodtranscomment} \n {prodremark} \n {fb_empserv} \n {fb_speed} \n {fb_clean} \n {servcomment} \n {servtranscomment} \n {servremark}'


                    msg = f'Subject: {subject}\n\n{body}'

                    smtp.sendmail(EMAIL_ADDRESS, 'johnchristophersinamban@gmail.com', msg)
                
                flash('Product & Service Feedback Added', category='success')
                
                
            elif servcompound >= 0.1:
                custname = request.form.get('custname')
                custcontact = request.form.get('custcontact')
                custemail = request.form.get('custemail')
                custstatus = request.form.get('custstatus')
                branch = request.form.get('branch')
                prodpurchase = request.form.getlist('prodpurchase')
                product =",".join(map(str, prodpurchase))

                fb_variety = request.form.get('fb_variety')
                fb_presentation = request.form.get('fb_presentation')
                fb_quality = request.form.get('fb_quality')
                prodcomment = request.form.get('prodcomment')
                prodremark = "Negative"
        
                fb_empserv = request.form.get('fb_empserv')
                fb_speed = request.form.get('fb_speed')
                fb_clean = request.form.get('fb_clean')
                servcomment = request.form.get('servcomment')
                servremark = "Posititve"
                
 
                new_servfb = Services(custname=custname, custcontact=custcontact, custemail=custemail, custstatus=custstatus, branch=branch, prodpurchase=product, fb_empserv=fb_empserv, fb_speed=fb_speed, fb_clean=fb_clean, servcomment=servcomment, servtranscomment=servtranscomment, servremark=servremark)
                new_prodservS = Prodserv(custname=custname, custcontact=custcontact, custemail=custemail, custstatus=custstatus, branch=branch, prodpurchase=product, fb_empserv=fb_empserv, fb_speed=fb_speed, fb_clean=fb_clean, servcomment=servcomment, servtranscomment=servtranscomment, servremark=servremark)                
                db.session.add(new_servfb)
                db.session.add(new_prodservS)

                new_prodfb = Products(custname=custname, custcontact=custcontact, custemail=custemail, custstatus=custstatus, branch=branch, prodpurchase=product, fb_variety=fb_variety, fb_presentation=fb_presentation, fb_quality=fb_quality, prodcomment=prodcomment, prodtranscomment=prodtranscomment, prodremark=prodremark)
                new_prodservP = Prodserv(custname=custname, custcontact=custcontact, custemail=custemail, custstatus=custstatus, branch=branch, prodpurchase=product, fb_variety=fb_variety, fb_presentation=fb_presentation, fb_quality=fb_quality, prodcomment=prodcomment, prodtranscomment=prodtranscomment, prodremark=prodremark)
                db.session.add(new_prodfb)
                db.session.add(new_prodservP)
                db.session.commit()
                EMAIL_ADDRESS = 'wecarekumparessystem@gmail.com'
                EMAIL_PASSWORD = 'jryhawyjeijnidge'

                with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                    smtp.ehlo()
                    smtp.starttls()
                    smtp.ehlo()

                    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                
                    subject = 'NEGATIVE FEEDBACK ALERT!'
                    body = f'Dear [Admin 1], \n A customer send a negative feedback about the product. Please review the feedback immediately. \n\n Feedback informations: \n {custname} \n {custcontact} \n {custemail} \n {custstatus} \n {branch} \n {prodpurchase} \n {fb_variety}\n {fb_presentation} \n {fb_quality} \n {prodcomment} \n {prodtranscomment} \n {prodremark}'


                    msg = f'Subject: {subject}\n\n{body}'

                    smtp.sendmail(EMAIL_ADDRESS, 'johnchristophersinamban@gmail.com', msg)
                
                flash('Product & Service Feedback Added', category='success')

            else:
                custname = request.form.get('custname')
                custcontact = request.form.get('custcontact')
                custemail = request.form.get('custemail')
                custstatus = request.form.get('custstatus')
                branch = request.form.get('branch')
                prodpurchase = request.form.getlist('prodpurchase')
                product =",".join(map(str, prodpurchase))

                fb_variety = request.form.get('fb_variety')
                fb_presentation = request.form.get('fb_presentation')
                fb_quality = request.form.get('fb_quality')
                prodcomment = request.form.get('prodcomment')
                prodremark = "Negative"
        
                fb_empserv = request.form.get('fb_empserv')
                fb_speed = request.form.get('fb_speed')
                fb_clean = request.form.get('fb_clean')
                servcomment = request.form.get('servcomment')
                servremark = "Neutral"
                
 
                new_servfb = Services(custname=custname, custcontact=custcontact, custemail=custemail, custstatus=custstatus, branch=branch, prodpurchase=product, fb_empserv=fb_empserv, fb_speed=fb_speed, fb_clean=fb_clean, servcomment=servcomment, servtranscomment=servtranscomment, servremark=servremark)
                new_prodservS = Prodserv(custname=custname, custcontact=custcontact, custemail=custemail, custstatus=custstatus, branch=branch, prodpurchase=product, fb_empserv=fb_empserv, fb_speed=fb_speed, fb_clean=fb_clean, servcomment=servcomment, servtranscomment=servtranscomment, servremark=servremark)                
                db.session.add(new_servfb)
                #db.session.add(new_prodservS)


                new_prodfb = Products(custname=custname, custcontact=custcontact, custemail=custemail, custstatus=custstatus, branch=branch, prodpurchase=product, fb_variety=fb_variety, fb_presentation=fb_presentation, fb_quality=fb_quality, prodcomment=prodcomment, prodtranscomment=prodtranscomment, prodremark=prodremark)
                new_prodservP = Prodserv(custname=custname, custcontact=custcontact, custemail=custemail, custstatus=custstatus, branch=branch, prodpurchase=product, fb_variety=fb_variety, fb_presentation=fb_presentation, fb_quality=fb_quality, prodcomment=prodcomment, prodtranscomment=prodtranscomment, prodremark=prodremark)
                db.session.add(new_prodfb)
                db.session.add(new_prodservP)
                db.session.commit()
                
                EMAIL_ADDRESS = 'wecarekumparessystem@gmail.com'
                EMAIL_PASSWORD = 'jryhawyjeijnidge'

                with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                    smtp.ehlo()
                    smtp.starttls()
                    smtp.ehlo()

                    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                
                    subject = 'NEGATIVE FEEDBACK ALERT!'
                    body = f'Dear [Admin 1], \n A customer send a negative feedback about the product. Please review the feedback immediately. \n\n Feedback informations: \n {custname} \n {custcontact} \n {custemail} \n {custstatus} \n {branch} \n {prodpurchase} \n {fb_variety}\n {fb_presentation} \n {fb_quality} \n {prodcomment} \n {prodtranscomment} \n {prodremark}'


                    msg = f'Subject: {subject}\n\n{body}'

                    smtp.sendmail(EMAIL_ADDRESS, 'johnchristophersinamban@gmail.com', msg)
                flash('Product & Service Feedback Added', category='success')
        elif prodcompound >= 0.1:
            if servcompound <= -0.1:
                custname = request.form.get('custname')
                custcontact = request.form.get('custcontact')
                custemail = request.form.get('custemail')
                custstatus = request.form.get('custstatus')
                branch = request.form.get('branch')
                prodpurchase = request.form.getlist('prodpurchase')
                product =",".join(map(str, prodpurchase))

                fb_variety = request.form.get('fb_variety')
                fb_presentation = request.form.get('fb_presentation')
                fb_quality = request.form.get('fb_quality')
                prodcomment = request.form.get('prodcomment')
                prodremark = "Positive"
        
                fb_empserv = request.form.get('fb_empserv')
                fb_speed = request.form.get('fb_speed')
                fb_clean = request.form.get('fb_clean')
                servcomment = request.form.get('servcomment')
                servremark = "Negative"
                
 
                new_servfb = Services(custname=custname, custcontact=custcontact, custemail=custemail, custstatus=custstatus, branch=branch, prodpurchase=product, fb_empserv=fb_empserv, fb_speed=fb_speed, fb_clean=fb_clean, servcomment=servcomment, servtranscomment=servtranscomment, servremark=servremark)
                new_prodservS = Prodserv(custname=custname, custcontact=custcontact, custemail=custemail, custstatus=custstatus, branch=branch, prodpurchase=product, fb_empserv=fb_empserv, fb_speed=fb_speed, fb_clean=fb_clean, servcomment=servcomment, servtranscomment=servtranscomment, servremark=servremark)                
                db.session.add(new_servfb)
                db.session.add(new_prodservS)

                new_prodfb = Products(custname=custname, custcontact=custcontact, custemail=custemail, custstatus=custstatus, branch=branch, prodpurchase=product, fb_variety=fb_variety, fb_presentation=fb_presentation, fb_quality=fb_quality, prodcomment=prodcomment, prodtranscomment=prodtranscomment, prodremark=prodremark)
                new_prodservP = Prodserv(custname=custname, custcontact=custcontact, custemail=custemail, custstatus=custstatus, branch=branch, prodpurchase=product, fb_variety=fb_variety, fb_presentation=fb_presentation, fb_quality=fb_quality, prodcomment=prodcomment, prodtranscomment=prodtranscomment, prodremark=prodremark)
                db.session.add(new_prodfb)
                db.session.add(new_prodservP)
                db.session.commit()
                
                EMAIL_ADDRESS = 'wecarekumparessystem@gmail.com'
                EMAIL_PASSWORD = 'jryhawyjeijnidge'

                with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                    smtp.ehlo()
                    smtp.starttls()
                    smtp.ehlo()

                    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                
                    subject = 'NEGATIVE FEEDBACK ALERT!'
                    body = f'Dear [Admin 1], \n A customer send a negative feedback about the service. Please review the feedback immediately. \n\n Feedback informations: \n {custname} \n {custcontact} \n {custemail} \n {custstatus} \n {branch} \n {prodpurchase} \n {fb_empserv}\n {fb_speed} \n {fb_clean} \n {servcomment} \n {servtranscomment} \n {servremark}'


                    msg = f'Subject: {subject}\n\n{body}'

                    smtp.sendmail(EMAIL_ADDRESS, 'johnchristophersinamban@gmail.com', msg)
                flash('Product & Service Feedback Added', category='success')
                
            elif servcompound >= 0.1:
                custname = request.form.get('custname')
                custcontact = request.form.get('custcontact')
                custemail = request.form.get('custemail')
                custstatus = request.form.get('custstatus')
                branch = request.form.get('branch')
                prodpurchase = request.form.getlist('prodpurchase')
                product =",".join(map(str, prodpurchase))

                fb_variety = request.form.get('fb_variety')
                fb_presentation = request.form.get('fb_presentation')
                fb_quality = request.form.get('fb_quality')
                prodcomment = request.form.get('prodcomment')
                prodremark = "Positive"
        
                fb_empserv = request.form.get('fb_empserv')
                fb_speed = request.form.get('fb_speed')
                fb_clean = request.form.get('fb_clean')
                servcomment = request.form.get('servcomment')
                servremark = "Posititve"
                
 
                new_servfb = Services(custname=custname, custcontact=custcontact, custemail=custemail, custstatus=custstatus, branch=branch, prodpurchase=product, fb_empserv=fb_empserv, fb_speed=fb_speed, fb_clean=fb_clean, servcomment=servcomment, servtranscomment=servtranscomment, servremark=servremark)
                new_prodservS = Prodserv(custname=custname, custcontact=custcontact, custemail=custemail, custstatus=custstatus, branch=branch, prodpurchase=product, fb_empserv=fb_empserv, fb_speed=fb_speed, fb_clean=fb_clean, servcomment=servcomment, servtranscomment=servtranscomment, servremark=servremark)                
                db.session.add(new_servfb)
                db.session.add(new_prodservS)

                new_prodfb = Products(custname=custname, custcontact=custcontact, custemail=custemail, custstatus=custstatus, branch=branch, prodpurchase=product, fb_variety=fb_variety, fb_presentation=fb_presentation, fb_quality=fb_quality, prodcomment=prodcomment, prodtranscomment=prodtranscomment, prodremark=prodremark)
                new_prodservP = Prodserv(custname=custname, custcontact=custcontact, custemail=custemail, custstatus=custstatus, branch=branch, prodpurchase=product, fb_variety=fb_variety, fb_presentation=fb_presentation, fb_quality=fb_quality, prodcomment=prodcomment, prodtranscomment=prodtranscomment, prodremark=prodremark)
                db.session.add(new_prodfb)
                db.session.add(new_prodservP)
                db.session.commit()
                flash('Product & Service Feedback Added', category='success')

            else:
                custname = request.form.get('custname')
                custcontact = request.form.get('custcontact')
                custemail = request.form.get('custemail')
                custstatus = request.form.get('custstatus')
                branch = request.form.get('branch')
                prodpurchase = request.form.getlist('prodpurchase')
                product =",".join(map(str, prodpurchase))

                fb_variety = request.form.get('fb_variety')
                fb_presentation = request.form.get('fb_presentation')
                fb_quality = request.form.get('fb_quality')
                prodcomment = request.form.get('prodcomment')
                prodremark = "Positive"
        
                fb_empserv = request.form.get('fb_empserv')
                fb_speed = request.form.get('fb_speed')
                fb_clean = request.form.get('fb_clean')
                servcomment = request.form.get('servcomment')
                servremark = "Neutral"
                
 
                new_servfb = Services(custname=custname, custcontact=custcontact, custemail=custemail, custstatus=custstatus, branch=branch, prodpurchase=product, fb_empserv=fb_empserv, fb_speed=fb_speed, fb_clean=fb_clean, servcomment=servcomment, servtranscomment=servtranscomment, servremark=servremark)
                new_prodservS = Prodserv(custname=custname, custcontact=custcontact, custemail=custemail, custstatus=custstatus, branch=branch, prodpurchase=product, fb_empserv=fb_empserv, fb_speed=fb_speed, fb_clean=fb_clean, servcomment=servcomment, servtranscomment=servtranscomment, servremark=servremark)                
                db.session.add(new_servfb)
                db.session.add(new_prodservS)

                new_prodfb = Products(custname=custname, custcontact=custcontact, custemail=custemail, custstatus=custstatus, branch=branch, prodpurchase=product, fb_variety=fb_variety, fb_presentation=fb_presentation, fb_quality=fb_quality, prodcomment=prodcomment, prodtranscomment=prodtranscomment, prodremark=prodremark)
                new_prodservP = Prodserv(custname=custname, custcontact=custcontact, custemail=custemail, custstatus=custstatus, branch=branch, prodpurchase=product, fb_variety=fb_variety, fb_presentation=fb_presentation, fb_quality=fb_quality, prodcomment=prodcomment, prodtranscomment=prodtranscomment, prodremark=prodremark)
                db.session.add(new_prodfb)
                db.session.add(new_prodservP)
                db.session.commit()
                flash('Product & Service Feedback Added', category='success')
    
        else:
            if servcompound <= -0.1:
                custname = request.form.get('custname')
                custcontact = request.form.get('custcontact')
                custemail = request.form.get('custemail')
                custstatus = request.form.get('custstatus')
                branch = request.form.get('branch')
                prodpurchase = request.form.getlist('prodpurchase')
                product =",".join(map(str, prodpurchase))

                fb_variety = request.form.get('fb_variety')
                fb_presentation = request.form.get('fb_presentation')
                fb_quality = request.form.get('fb_quality')
                prodcomment = request.form.get('prodcomment')
                prodremark = "Neutral"
        
                fb_empserv = request.form.get('fb_empserv')
                fb_speed = request.form.get('fb_speed')
                fb_clean = request.form.get('fb_clean')
                servcomment = request.form.get('servcomment')
                servremark = "Negative"
                
 
                new_servfb = Services(custname=custname, custcontact=custcontact, custemail=custemail, custstatus=custstatus, branch=branch, prodpurchase=product, fb_empserv=fb_empserv, fb_speed=fb_speed, fb_clean=fb_clean, servcomment=servcomment, servtranscomment=servtranscomment, servremark=servremark)
                new_prodservS = Prodserv(custname=custname, custcontact=custcontact, custemail=custemail, custstatus=custstatus, branch=branch, prodpurchase=product, fb_empserv=fb_empserv, fb_speed=fb_speed, fb_clean=fb_clean, servcomment=servcomment, servtranscomment=servtranscomment, servremark=servremark)                
                db.session.add(new_servfb)
                db.session.add(new_prodservS)

                new_prodfb = Products(custname=custname, custcontact=custcontact, custemail=custemail, custstatus=custstatus, branch=branch, prodpurchase=product, fb_variety=fb_variety, fb_presentation=fb_presentation, fb_quality=fb_quality, prodcomment=prodcomment, prodtranscomment=prodtranscomment, prodremark=prodremark)
                new_prodservP = Prodserv(custname=custname, custcontact=custcontact, custemail=custemail, custstatus=custstatus, branch=branch, prodpurchase=product, fb_variety=fb_variety, fb_presentation=fb_presentation, fb_quality=fb_quality, prodcomment=prodcomment, prodtranscomment=prodtranscomment, prodremark=prodremark)
                db.session.add(new_prodfb)
                db.session.add(new_prodservP)
                db.session.commit()
                
                EMAIL_ADDRESS = 'wecarekumparessystem@gmail.com'
                EMAIL_PASSWORD = 'jryhawyjeijnidge'

                with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                    smtp.ehlo()
                    smtp.starttls()
                    smtp.ehlo()

                    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                
                    subject = 'NEGATIVE FEEDBACK ALERT!'
                    body = f'Dear [Admin 1], \n A customer send a negative feedback about the service. Please review the feedback immediately. \n\n Feedback informations: \n {custname} \n {custcontact} \n {custemail} \n {custstatus} \n {branch} \n {prodpurchase} \n {fb_empserv}\n {fb_speed} \n {fb_clean} \n {servcomment} \n {servtranscomment} \n {servremark}'


                    msg = f'Subject: {subject}\n\n{body}'

                    smtp.sendmail(EMAIL_ADDRESS, 'johnchristophersinamban@gmail.com', msg)
                flash('Product & Service Feedback Added', category='success')
                
            elif servcompound >= 0.1:
                custname = request.form.get('custname')
                custcontact = request.form.get('custcontact')
                custemail = request.form.get('custemail')
                custstatus = request.form.get('custstatus')
                branch = request.form.get('branch')
                prodpurchase = request.form.getlist('prodpurchase')
                product =",".join(map(str, prodpurchase))

                fb_variety = request.form.get('fb_variety')
                fb_presentation = request.form.get('fb_presentation')
                fb_quality = request.form.get('fb_quality')
                prodcomment = request.form.get('prodcomment')
                prodremark = "Neutral"
        
                fb_empserv = request.form.get('fb_empserv')
                fb_speed = request.form.get('fb_speed')
                fb_clean = request.form.get('fb_clean')
                servcomment = request.form.get('servcomment')
                servremark = "Posititve"
                
 
                new_servfb = Services(custname=custname, custcontact=custcontact, custemail=custemail, custstatus=custstatus, branch=branch, prodpurchase=product, fb_empserv=fb_empserv, fb_speed=fb_speed, fb_clean=fb_clean, servcomment=servcomment, servtranscomment=servtranscomment, servremark=servremark)
                new_prodservS = Prodserv(custname=custname, custcontact=custcontact, custemail=custemail, custstatus=custstatus, branch=branch, prodpurchase=product, fb_empserv=fb_empserv, fb_speed=fb_speed, fb_clean=fb_clean, servcomment=servcomment, servtranscomment=servtranscomment, servremark=servremark)                
                db.session.add(new_servfb)
                db.session.add(new_prodservS)

                new_prodfb = Products(custname=custname, custcontact=custcontact, custemail=custemail, custstatus=custstatus, branch=branch, prodpurchase=product, fb_variety=fb_variety, fb_presentation=fb_presentation, fb_quality=fb_quality, prodcomment=prodcomment, prodtranscomment=prodtranscomment, prodremark=prodremark)
                new_prodservP = Prodserv(custname=custname, custcontact=custcontact, custemail=custemail, custstatus=custstatus, branch=branch, prodpurchase=product, fb_variety=fb_variety, fb_presentation=fb_presentation, fb_quality=fb_quality, prodcomment=prodcomment, prodtranscomment=prodtranscomment, prodremark=prodremark)
                db.session.add(new_prodfb)
                db.session.add(new_prodservP)
                db.session.commit()
                flash('Product & Service Feedback Added', category='success')

            else:
                custname = request.form.get('custname')
                custcontact = request.form.get('custcontact')
                custemail = request.form.get('custemail')
                custstatus = request.form.get('custstatus')
                branch = request.form.get('branch')
                prodpurchase = request.form.getlist('prodpurchase')
                product =",".join(map(str, prodpurchase))

                fb_variety = request.form.get('fb_variety')
                fb_presentation = request.form.get('fb_presentation')
                fb_quality = request.form.get('fb_quality')
                prodcomment = request.form.get('prodcomment')
                prodremark = "Neutral"
        
                fb_empserv = request.form.get('fb_empserv')
                fb_speed = request.form.get('fb_speed')
                fb_clean = request.form.get('fb_clean')
                servcomment = request.form.get('servcomment')
                servremark = "Neutral"
                
 
                new_servfb = Services(custname=custname, custcontact=custcontact, custemail=custemail, custstatus=custstatus, branch=branch, prodpurchase=product, fb_empserv=fb_empserv, fb_speed=fb_speed, fb_clean=fb_clean, servcomment=servcomment, servtranscomment=servtranscomment, servremark=servremark)
                new_prodservS = Prodserv(custname=custname, custcontact=custcontact, custemail=custemail, custstatus=custstatus, branch=branch, prodpurchase=product, fb_empserv=fb_empserv, fb_speed=fb_speed, fb_clean=fb_clean, servcomment=servcomment, servtranscomment=servtranscomment, servremark=servremark)                
                db.session.add(new_servfb)
                db.session.add(new_prodservS)

                new_prodfb = Products(custname=custname, custcontact=custcontact, custemail=custemail, custstatus=custstatus, branch=branch, prodpurchase=product, fb_variety=fb_variety, fb_presentation=fb_presentation, fb_quality=fb_quality, prodcomment=prodcomment, prodtranscomment=prodtranscomment, prodremark=prodremark)
                new_prodservP = Prodserv(custname=custname, custcontact=custcontact, custemail=custemail, custstatus=custstatus, branch=branch, prodpurchase=product, fb_variety=fb_variety, fb_presentation=fb_presentation, fb_quality=fb_quality, prodcomment=prodcomment, prodtranscomment=prodtranscomment, prodremark=prodremark)
                db.session.add(new_prodfb)
                db.session.add(new_prodservP)
                db.session.commit()
                flash('Product & Service Feedback Added', category='success')

    all_prod = Products.query.all()
    all_serv = Services.query.all()
    return render_template("prodservform.html", prod = all_prod, serv = all_serv)


@views.route('/servform', methods=["GET", "POST"])
def serv():
    translator = Translator()
    if request.method == "POST":
        servcomment = request.form.get('servcomment')
        trans = translator.translate(servcomment, src="tl", dest="en")
        sid = SentimentIntensityAnalyzer()
        score = sid.polarity_scores(trans.text)
        compound = score['compound']
        servtranscomment = trans.text
        if compound <= -0.1:
            
            custname = request.form.get('custname')
            custcontact = request.form.get('custcontact')
            custemail = request.form.get('custemail')
            custstatus = request.form.get('custstatus')
            branch = request.form.get('branch')
            prodpurchase = request.form.getlist('prodpurchase')
            product =",".join(map(str, prodpurchase))
            fb_empserv = request.form.get('fb_empserv')
            fb_speed = request.form.get('fb_speed')
            fb_clean = request.form.get('fb_clean')
            servcomment = request.form.get('servcomment')
            servremark = "Negative"
 
            new_servfb = Services(custname=custname, custcontact=custcontact, custemail=custemail, custstatus=custstatus, branch=branch, prodpurchase=product, fb_empserv=fb_empserv, fb_speed=fb_speed, fb_clean=fb_clean, servcomment=servcomment, servtranscomment=servtranscomment, servremark=servremark)
            new_prodservS = Prodserv(custname=custname, custcontact=custcontact, custemail=custemail, custstatus=custstatus, branch=branch, prodpurchase=product, fb_empserv=fb_empserv, fb_speed=fb_speed, fb_clean=fb_clean, servcomment=servcomment, servtranscomment=servtranscomment, servremark=servremark)                
            db.session.add(new_servfb)
            db.session.add(new_prodservS)
            db.session.commit()
            
            EMAIL_ADDRESS = 'wecarekumparessystem@gmail.com'
            EMAIL_PASSWORD = 'jryhawyjeijnidge'

            with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                    smtp.ehlo()
                    smtp.starttls()
                    smtp.ehlo()

                    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                
                    subject = 'NEGATIVE FEEDBACK ALERT!'
                    body = f'Dear [Admin 1], \n A customer send a negative feedback about the service. Please review the feedback immediately. \n\n Feedback informations: \n {custname} \n {custcontact} \n {custemail} \n {custstatus} \n {branch} \n {prodpurchase} \n {fb_empserv}\n {fb_speed} \n {fb_clean} \n {servcomment} \n {servtranscomment} \n {servremark}'


                    msg = f'Subject: {subject}\n\n{body}'

                    smtp.sendmail(EMAIL_ADDRESS, 'johnchristophersinamban@gmail.com', msg)
            flash('Product Feedback Added', category='success')
            
        elif compound >= 0.1:
            custname = request.form.get('custname')
            custcontact = request.form.get('custcontact')
            custemail = request.form.get('custemail')
            custstatus = request.form.get('custstatus')
            branch = request.form.get('branch')
            prodpurchase = request.form.getlist('prodpurchase')
            product =",".join(map(str, prodpurchase))
            fb_empserv = request.form.get('fb_empserv')
            fb_speed = request.form.get('fb_speed')
            fb_clean = request.form.get('fb_clean')
            servcomment = request.form.get('servcomment')
            servremark = "Positive"
            
            new_servfb = Services(custname=custname, custcontact=custcontact, custemail=custemail, custstatus=custstatus, branch=branch, prodpurchase=product, fb_empserv=fb_empserv, fb_speed=fb_speed, fb_clean=fb_clean, servcomment=servcomment, servtranscomment=servtranscomment, servremark=servremark)
            new_prodservS = Prodserv(custname=custname, custcontact=custcontact, custemail=custemail, custstatus=custstatus, branch=branch, prodpurchase=product, fb_empserv=fb_empserv, fb_speed=fb_speed, fb_clean=fb_clean, servcomment=servcomment, servtranscomment=servtranscomment, servremark=servremark)                
            db.session.add(new_servfb)
            db.session.add(new_prodservS)
            db.session.commit()
            flash('Product Feedback Added', category='success')
            
        else:
            custname = request.form.get('custname')
            custcontact = request.form.get('custcontact')
            custemail = request.form.get('custemail')
            custstatus = request.form.get('custstatus')
            branch = request.form.get('branch')
            prodpurchase = request.form.getlist('prodpurchase')
            product =",".join(map(str, prodpurchase))
            fb_empserv = request.form.get('fb_empserv')
            fb_speed = request.form.get('fb_speed')
            fb_clean = request.form.get('fb_clean')
            servcomment = request.form.get('servcomment')
            servremark = "Neutral"
            
            new_servfb = Services(custname=custname, custcontact=custcontact, custemail=custemail, custstatus=custstatus, branch=branch, prodpurchase=product, fb_empserv=fb_empserv, fb_speed=fb_speed, fb_clean=fb_clean, servcomment=servcomment, servtranscomment=servtranscomment, servremark=servremark)
            new_prodservS = Prodserv(custname=custname, custcontact=custcontact, custemail=custemail, custstatus=custstatus, branch=branch, prodpurchase=product, fb_empserv=fb_empserv, fb_speed=fb_speed, fb_clean=fb_clean, servcomment=servcomment, servtranscomment=servtranscomment, servremark=servremark)                
            db.session.add(new_servfb)
            db.session.add(new_prodservS)
            db.session.commit()
            flash('Product Feedback Added', category='success')
           
    all_serv = Services.query.all()
    return render_template("servform.html", serv = all_serv)

@views.route('/menu')
def menu():
    return render_template("menu.html")

@views.route('/chickenmenu')
def chickenmenu():
    return render_template("chickenmenu.html")

@views.route('/porkmenu')
def porkmenu():
    return render_template("porkmenu.html")

@views.route('/beefmenu')
def beefmenu():
    return render_template("beefmenu.html")

@views.route('/ricemeals')
def ricemeals():
    return render_template("ricemeals.html")

@views.route('/beverages')
def beverages():
    return render_template("beverages.html")

@views.route('/bundles')
def bundles():
    return render_template("bundles.html")

@views.route('/admin')
@login_required
def admin():
    prodserv = Prodserv.query.all()
    
    date = "2022-10-28"

    total = db.session.query(db.func.count(Prodserv.custname)).all()
    t_count = np.array(total).astype('int')
    total_count = int(t_count)
    s = db.session.query(db.func.count(Prodserv.date_added)).filter(Prodserv.date_added==date).all()
    e = db.session.query(db.func.count(Prodserv.date_added)).filter((Prodserv.date_added == date) & (Prodserv.custstatus=="old customer")).all()
    start = np.array(s).astype('int')
    end = np.array(e).astype('int')
    start_cus = int(start)
    end_cus = int(end)
    cus_retention = (int(end_cus)/int(start_cus)) *100
    cus_ret = round(cus_retention,2)

    branch_comparison = db.session.query(db.func.count(Prodserv.custname), Prodserv.branch).group_by(Prodserv.branch).order_by(Prodserv.branch).all()

    status_comparison = db.session.query(db.func.count(Prodserv.custname), Prodserv.custstatus).group_by(Prodserv.custstatus).order_by(Prodserv.custstatus).all()

    branch_category = []
    for branch, _ in branch_comparison:
        branch_category.append(branch)

    status_category = []
    for status, _ in status_comparison:
        status_category.append(status)
    
    return render_template("admin.html",
                           total_count = total_count, 
                           start_cus=start_cus,
                           end_cus=end_cus,
                           cus_ret = cus_ret,
                           branch_category=json.dumps(branch_category),
                           status_category=json.dumps(status_category),
                           prodserv = prodserv, user=current_user)

@views.route('/profile')
@login_required
def profile():
    return render_template("profile.html", user=current_user)

@views.route('/prodfeedback')
@login_required
def prodfeedback():
    prod = Products.query.all()

    productremarks = db.session.query(db.func.count(Products.custname), Products.prodremark).group_by(Products.prodremark).order_by(Products.prodremark).all()

    branch_comparison = db.session.query(db.func.count(Products.custname), Products.branch).group_by(Products.branch).order_by(Products.branch).all()

    status_comparison = db.session.query(db.func.count(Products.custname), Products.custstatus).group_by(Products.custstatus).order_by(Products.custstatus).all()

    dates = db.session.query(db.func.sum(Products.custname), Products.date_added).group_by(Products.date_added).order_by(Products.date_added).all()

    branch_category = []
    for branch, _ in branch_comparison:
        branch_category.append(branch)

    status_category = []
    for status, _ in status_comparison:
        status_category.append(status)

    remark = []
    for prodremarks, _ in productremarks:
        remark.append(prodremarks)

    date_add = []
    dates_label = []
    for custname, date_added in dates:
        dates_label.append(date_added.strftime("%m-%d-%y"))
        date_add.append(custname)

    return render_template('prodfeedback.html',
                            productremarks=json.dumps(remark),
                            branch_category=json.dumps(branch_category),
                            status_category=json.dumps(status_category),
                            date_add=json.dumps(date_add),
                            dates_label =json.dumps(dates_label),
                            prod = prod, user=current_user
                        )
#    return render_template("feedback.html", prod = prod, user=current_user)

@views.route('/servfeedback')
@login_required
def servfeedback():
    serv = Services.query.all()

    servicesremarks = db.session.query(db.func.count(Services.custname), Services.servremark).group_by(Services.servremark).order_by(Services.servremark).all()

    branch_comparison = db.session.query(db.func.count(Services.custname), Services.branch).group_by(Services.branch).order_by(Services.branch).all()

    status_comparison = db.session.query(db.func.count(Services.custname), Services.custstatus).group_by(Services.custstatus).order_by(Services.custstatus).all()

    dates = db.session.query(db.func.sum(Services.custname), Services.date_added).group_by(Services.date_added).order_by(Services.date_added).all()

    branch_category = []
    for branch, _ in branch_comparison:
        branch_category.append(branch)

    status_category = []
    for status, _ in status_comparison:
        status_category.append(status)

    remark = []
    for servremarks, _ in servicesremarks:
        remark.append(servremarks)

    date_add = []
    dates_label = []
    for custname, date_added in dates:
        dates_label.append(date_added.strftime("%m-%d-%y"))
        date_add.append(custname)

    return render_template('servfeedback.html',
                            servicesremarks=json.dumps(remark),
                            branch_category=json.dumps(branch_category),
                            status_category=json.dumps(status_category),
                            date_add=json.dumps(date_add),
                            dates_label =json.dumps(dates_label),
                            serv = serv, user=current_user
                        )
#    return render_template("feedback.html", prod = prod, user=current_user)

@views.route('/edit/<int:id>', methods=['GET','POST'])
def edit(id):
    prod = Products.query.filter_by(id=id).first()

    if request.method == 'POST':

        prod.custname = request.form.get('custname')
        prod.custstatus = request.form.get('custstatus')
        prod.branch = request.form.get('branch')
        prod.prodpurchase = request.form.get('prodpurchase')
        prod.fb_variety = request.form.get('fb_variety')
        prod.fb_presentation = request.form.get('fb_presentation')
        prod.fb_quality = request.form.get('fb_quality')
        prod.prodcomment = request.form.get('prodcomment')
        prod.prodremark = request.form.get('prodremark')

        try:
            db.session.commit()
            return redirect('/feedback')
        except:
            return "There was a problem"
    else:

        return render_template("editFeedback.html", prod = prod)
 

 
@views.route('/delete/<int:id>', methods=['GET','POST'])
def delete(id):
    prod = Products.query.filter_by(id=id).first()
    if request.method == 'POST':
        if prod:
            db.session.delete(prod)
            db.session.commit()
            return redirect('/feedback')

    return render_template("deleteFeedback.html", prod = prod)

@views.route('/edits/<int:id>', methods=['GET','POST'])
def edits(id):
    serv = Services.query.filter_by(id=id).first()

    if request.method == 'POST':

        serv.custname = request.form.get('custname')
        serv.custstatus = request.form.get('custstatus')
        serv.branch = request.form.get('branch')
        serv.prodpurchase = request.form.get('prodpurchase')
        serv.fb_empserv = request.form.get('fb_empserv')
        serv.fb_speed = request.form.get('fb_speed')
        serv.fb_clean = request.form.get('fb_clean')
        serv.servcomment = request.form.get('servcomment')
        serv.servremark = request.form.get('servremark')

        try:
            db.session.commit()
            return redirect('/servfeedback')
        except:
            return "There was a problem"
    else:

        return render_template("editFeedbackS.html", serv = serv)
 

 
@views.route('/deletes/<int:id>', methods=['GET','POST'])
def deletes(id):
    serv = Services.query.filter_by(id=id).first()
    if request.method == 'POST':
        if prod:
            db.session.delete(serv)
            db.session.commit()
            return redirect('/servfeedback')

    return render_template("deleteFeedbackS.html", serv = serv)
    
#@views.route('/settings')
#def settings():
#    all_admin = Admin.query.all()

#    return render_template("settings.html", admins = all_admin)


@views.route('/csatprod')
@login_required
def csatprod():
    prod = Products.query.all()
    
    total_count = db.session.query(db.func.count(Products.custname)).all()
    variety_count = db.session.query(db.func.count(Products.fb_variety)).filter((Products.fb_variety==4) | (Products.fb_variety==5)).all()
    variety_cnt = np.array(variety_count).astype('int')
    vartotal = np.array(total_count).astype('int')
    v = (variety_cnt/vartotal)*100
    var_score = float(v)
    variety_score = round(var_score,2)
    v_score = int(v)
    
    if variety_score in range(75,85):
        variety_reccomendation = "Great Job! Your product variety satisfaction score is in the a great position, keep it up!"
    elif variety_score < 75:
        variety_reccomendation = "Oh No! It seems like a lot of customer think that your product variety needs to be improve. Try expanding your menu for your customer to be satisfied on product variety!"
    elif variety_score > 85:
        variety_reccomendation = "Superb! Your product variety satisfaction score is remarkable, maintain your strategy!"
        
        
    presentation_count = db.session.query(db.func.count(Products.fb_presentation)).filter((Products.fb_presentation==4) | (Products.fb_presentation==5)).all()
    presentation_cnt = np.array(presentation_count).astype('int')
    prestotal = np.array(total_count).astype('int')
    p = (presentation_cnt/prestotal)*100
    pres_score = float(p)
    presentation_score = round(pres_score,2)
    
    if presentation_score in range(75,85):
        presentation_reccomendation = "Great Job! Your product presentation satisfaction score is in the a great position, keep it up!"
    elif presentation_score < 75:
        presentation_reccomendation = "Oh No! It seems like a lot of customer think that your product presentation needs to be improve. Try expanding your menu for your customer to be satisfied on product variety!"
    elif presentation_score > 85:
        presentation_reccomendation = "Superb! Your product presentation satisfaction score is remarkable, maintain your strategy!"
    
    quality_count = db.session.query(db.func.count(Products.fb_quality)).filter((Products.fb_quality==4) | (Products.fb_quality==5)).all()
    quality_cnt = np.array(quality_count).astype('int')
    qlytotal = np.array(total_count).astype('int')
    q = (quality_cnt/qlytotal)*100
    qual_score = float(q)
    quality_score = round(qual_score,2)
    
    if quality_score in range(75,85):
        quality_reccomendation = "Great Job! Your product quality satisfaction score is in the a great position, keep it up!"
    elif quality_score < 75:
        quality_reccomendation = "Oh No! It seems like a lot of customer think that your product quality needs to be improve. Try expanding your menu for your customer to be satisfied on product variety!"
    elif quality_score > 85:
        quality_reccomendation = "Superb! Your product quality satisfaction score is remarkable, maintain your strategy!"
    
    
    variety_comparison = db.session.query(db.func.count(Products.custname), Products.fb_variety).group_by(Products.fb_variety).order_by(Products.fb_variety).all()

    presentation_comparison = db.session.query(db.func.count(Products.custname), Products.fb_presentation).group_by(Products.fb_presentation).order_by(Products.fb_presentation).all()

    quality_comparison = db.session.query(db.func.count(Products.custname), Products.fb_quality).group_by(Products.fb_quality).order_by(Products.fb_quality).all()
    
    variety_category = []
    for variety, _ in variety_comparison:
        variety_category.append(variety)

    presentation_category = []
    for presentation, _ in presentation_comparison:
        presentation_category.append(presentation)

    quality_category = []
    for quality, _ in quality_comparison:
        quality_category.append(quality)


    return render_template('csatprod.html',
                            variety_category=json.dumps(variety_category),
                            presentation_category=json.dumps(presentation_category),
                            quality_category=json.dumps(quality_category),
                            variety_score = variety_score,
                            variety_reccomendation = variety_reccomendation,
                            presentation_score = presentation_score,
                            presentation_reccomendation =  presentation_reccomendation,
                            quality_score = quality_score,
                            quality_reccomendation = quality_reccomendation,
                            v_score = v_score,
                            prod = prod, user=current_user
                        )

#    return render_template("feedback.html", prod = prod, user=current_user)

@views.route('/csatserv')
@login_required
def csatserv():
    serv = Services.query.all()
    
    total_count = db.session.query(db.func.count(Services.custname)).all()
    empserv_count = db.session.query(db.func.count(Services.fb_empserv)).filter((Services.fb_empserv==4) | (Services.fb_empserv==5)).all()
    empserv_cnt = np.array(empserv_count).astype('int')
    empservtotal = np.array(total_count).astype('int')
    e = (empserv_cnt/empservtotal) *100
    es_score = float(e)
    empserv_score = round(es_score,2)
    
    if empserv_score in range(75,85):
       empserv_reccomendation = "Great Job! Your Employee Service satisfaction score is in the a great position, keep it up!"
    elif empserv_score < 75:
        empserv_reccomendation = "Oh No! It seems like a lot of customer think that your Employee Service needs to be improve. Try expanding your menu for your customer to be satisfied on product variety!"
    elif empserv_score > 85:
        empserv_reccomendation = "Superb! Your Employee Service satisfaction score is remarkable, maintain your strategy!"
        
    
    speed_count = db.session.query(db.func.count(Services.fb_speed)).filter((Services.fb_speed==4) | (Services.fb_speed==5)).all()
    speed_cnt = np.array(speed_count).astype('int')
    speedtotal = np.array(total_count).astype('int')
    s = (speed_cnt/speedtotal) *100
    spd_score = float(s)
    speed_score = round(spd_score,2)
    
    if speed_score in range(75,85):
       speed_reccomendation = "Great Job! Your speed of service satisfaction score is in the a great position, keep it up!"
    elif speed_score < 75:
        speed_reccomendation = "Oh No! It seems like a lot of customer think that your speed of service needs to be improve. Try expanding your menu for your customer to be satisfied on product variety!"
    elif speed_score > 85:
        speed_reccomendation = "Superb! Your speed of service satisfaction score is remarkable, maintain your strategy!"
        
    
    clean_count = db.session.query(db.func.count(Services.fb_clean)).filter((Services.fb_clean==4) | (Services.fb_clean==5)).all()
    clean_cnt = np.array(clean_count).astype('int')
    cleantotal = np.array(total_count).astype('int')
    c = (clean_cnt/cleantotal) *100
    cln_score = float(c)
    clean_score = round(cln_score,2)
    
    if clean_score in range(75,85):
       clean_reccomendation = "Great Job! Your store cleanliness satisfaction score is in the a great position, keep it up!"
    elif clean_score < 75:
        clean_reccomendation = "Oh No! It seems like a lot of customer think that your store cleanliness needs to be improve. Try expanding your menu for your customer to be satisfied on product variety!"
    elif clean_score > 85:
        clean_reccomendation = "Superb! Your store cleanliness satisfaction score is remarkable, maintain your strategy!"
        

    empserv_comparison = db.session.query(db.func.count(Services.custname), Services.fb_empserv).group_by(Services.fb_empserv).order_by(Services.fb_empserv).all()

    speed_comparison = db.session.query(db.func.count(Services.custname), Services.fb_speed).group_by(Services.fb_speed).order_by(Services.fb_speed).all()

    clean_comparison = db.session.query(db.func.count(Services.custname), Services.fb_clean).group_by(Services.fb_clean).order_by(Services.fb_clean).all()

    empserv_category = []
    for empserv, _ in empserv_comparison:
        empserv_category.append(empserv)

    speed_category = []
    for speed, _ in speed_comparison:
        speed_category.append(speed)

    clean_category = []
    for clean, _ in clean_comparison:
        clean_category.append(clean)


    return render_template('csatserv.html',
                            empserv_category=json.dumps(empserv_category),
                            speed_category=json.dumps(speed_category),
                            clean_category=json.dumps(clean_category),
                            empserv_score = empserv_score,
                            empserv_reccomendation = empserv_reccomendation,
                            speed_score = speed_score,
                            speed_reccomendation = speed_reccomendation,
                            clean_score = clean_score,
                            clean_reccomendation = clean_reccomendation,
                            serv = serv, user=current_user
                        )

@views.route('/samplecode')
def samplecode():
    return render_template("samplecode.html")