from flask import render_template, request, jsonify, abort
from flask_mail import  Message
from sqlalchemy import desc
from math import floor
from flask_security import current_user

from model import *
from settings import app, mail
# Flask views
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact')
def contact_us():
    return render_template('contact.html')

@app.route('/rates', methods=['GET', 'POST'])
def rates():
    if request.method == 'GET':
        user=current_user
        posts = Review.query.order_by(desc(Review.date))
        review_amounts=len(posts.all())
        return render_template('rates.html', posts=posts, review_amounts=review_amounts )
    if request.method == 'POST':
        params = request.get_json()
        user = current_user

        if params['type'] == 'comment':
            posts = Review.query.order_by(desc(Review.date))
            res = {}

            if user.is_authenticated() and not user.has_role('blocked'):
                lastusercomment=posts.filter_by(user=user).first()
                stringcheker=params['text'].replace(' ', '')
                if lastusercomment==None:
                    if stringcheker:
                        #adding new
                        post = Review(text=params['text'], user=user)
                        db.session.add(post)
                        db.session.commit()
                        res['status']='ok'
                    else:
                        res['notification'] = render_template('_notification.html', text="Please enter some text")

                else:
                    delta=datetime.datetime.now() - lastusercomment.date
                    time_in_seconds=delta.total_seconds()
                    delta=floor(delta.total_seconds() /60)
                    if delta>= 1:
                        if stringcheker:
                            post = Review(text=params['text'], user=user)
                            db.session.add(post)
                            db.session.commit()
                            res['status']='ok'
                        else:
                            res['notification'] = render_template('_notification.html', text="Please enter some text")
                    else:
                        time_to_wait=60 - time_in_seconds
                        res['notification'] = render_template('_notification.html', text='Sorry! Wait {0} more seconds'.format(time_to_wait))
                        res['status']='failed'
            else:
                if not user.is_authenticated():
                    res['notification'] = render_template('_notification.html', text="Sorry, you are not authenticated!")
                elif user.has_role('blocked'):
                    res['notification'] = render_template('_notification.html', text="Sorry, you are in the blacklist!")

            review_amounts=len(posts.all())
            return jsonify(markup=render_template('comment-list.html', posts=posts), review_amounts=review_amounts, **res)



@app.route('/interpreters')
def translators():
    translators=Translator.query.all()
    return render_template('translators.html', translators=translators)

@app.route('/services')
def services():
    services=Service.query.all()
    return render_template('services.html', services=services)

@app.route('/services/<servicename>', methods=['GET', 'POST'])
def services_service(servicename):
    if request.method == 'GET':
        service=Service.query.filter(Service.slug==servicename).first()
        user=current_user
        if user.is_authenticated() and not user.has_role('blocked'):
            like = LikeService.query.filter_by(service=service, user=user).first()
            if like:
                liked = True
            else:
                liked = False
        else:
            liked = False
        if service==None:
            abort(404)
        count=len(service.images)
        posts = PostService.query.filter_by(service=service)
        posts = posts.order_by(desc(PostService.date))
        return render_template('service.html', service=service, count=count, already_liked=liked, posts=posts)

    if request.method == 'POST':
        params = request.get_json()
        service = Service.query.filter(Service.slug==params['service']).first()
        user = current_user
        res = {}
        if params['type'] == 'like':
            if user.is_authenticated() and not user.has_role('blocked'):
                like = LikeService.query.filter_by(service=service, user=user).first()
                if like:
                    refuse = True
                    db.session.delete(like)
                else:
                    refuse = False
                    like = LikeService(service=service, user=user)
                    db.session.add(like)
                db.session.commit()
            else:
                refuse = True
                if not user.is_authenticated():
                    res['notification'] = render_template('_notification.html', text="Sorry, you are not authenticated!")
                elif user.has_role('blocked'):
                    res['notification'] = render_template('_notification.html', text="Sorry, you are in the blacklist!")
            return jsonify(likes_amount=service.likes_amount, refuse_like=refuse, **res)

        if params['type'] == 'comment':
            posts = PostService.query.filter_by(service=service)
            posts = posts.order_by(desc(PostService.date))
            res= {}
            if user.is_authenticated() and not user.has_role('blocked'):
                lastusercomment=posts.filter_by(user=user).first()
                stringcheker=params['text'].replace(' ', '')
                if lastusercomment ==None:
                    #adding new

                    if stringcheker:
                        post = PostService(text=params['text'], service=service, user=user)
                        db.session.add(post)
                        db.session.commit()
                        res['status']='ok'
                    else:
                        res['notification'] = render_template('_notification.html', text="Please enter some text")

                else:
                    delta=datetime.datetime.now() - lastusercomment.date
                    time_in_seconds=delta.total_seconds()
                    delta=floor(delta.total_seconds() /60)
                    if delta>= 1:
                        if stringcheker:
                            post=PostService(text=params['text'] , service=service, user=user)
                            db.session.add(post)
                            db.session.commit()
                            res['status']='ok'
                        else:
                            res['notification'] = render_template('_notification.html', text="Please enter some text")
                    else:
                        time_to_wait=60 - time_in_seconds
                        res['notification'] = render_template('_notification.html', text='Sorry! Wait {0} more seconds'.format(time_to_wait))
                        res['status']='failed'
            else:
                if not user.is_authenticated():
                    res['notification'] = render_template('_notification.html', text="Sorry, you are not authenticated!")
                elif user.has_role('blocked'):
                    res['notification'] = render_template('_notification.html', text="Sorry, you are in the blacklist!")
            comments=service.comments_amount
            return jsonify(markup=render_template('comment-list.html', posts=posts),comment_amount=comments, **res)


@app.route('/business')
def business():
    services=Service.query.filter(Service.type=='Business').all()
    return render_template('business.html', services=services)

@app.route('/entertainment')
def entertainment():
    services=Service.query.filter(Service.type=='Entertainment').all()
    return render_template('entertainment.html', services=services)

@app.route('/excursions')
def excursions():
    services=Service.query.filter(Service.type=='Excursions').all()
    return render_template('excursions.html', services=services)

@app.route("/service/mail", methods=['POST'])
def send_mail_from_translator():
    data = request.get_json()
    if current_user.is_authenticated() and not current_user.has_role('blocked'):
        translator=Translator.query.filter(Translator.slug==data['translator']).first()
        data['translator'] = translator.first_name+" "+translator.last_name
        data['user'] = current_user.email
        data['date'] = datetime.datetime.now()

        mail_template = render_template('service-mail.jinja', **data)

        msg = Message('new service',
                      sender="user@example.com",
                      recipients=["user@example.com"])
        msg.body = mail_template
        mail.send(msg)
        return jsonify(**{'status':'ok', 'notification': render_template('_notification.html', text="We have recived your service offer. We will contact you soon.")})
    else:
        if not current_user.is_authenticated():
            return jsonify(**{'status':'fail', 'notification': render_template('_notification.html', text="Sorry, you are not authenticated!")})
        elif current_user.has_role('blocked'):
            return jsonify(**{'status':'fail', 'notification': render_template('_notification.html', text="Sorry, you are in the blacklist!")})

@app.route("/translator/mail", methods=['POST'])
def send_mail_from_service():
    data = request.get_json()
    if current_user.is_authenticated() and not current_user.has_role('blocked'):
        service=Service.query.filter(Service.slug==data['service']).first()
        data['service'] = service.name
        data['user'] = current_user.email
        data['date'] = datetime.datetime.now()

        mail_template = render_template('service-mail.jinja', **data)

        msg = Message('new service',
                      sender="user@example.com",
                      recipients=["user@example.com"])
        msg.body = mail_template
        mail.send(msg)
        return jsonify(**{'status':'ok', 'notification': render_template('_notification.html', text="We have recived your service offer. We will contact you soon.")})
    else:
        if not current_user.is_authenticated():
            return jsonify(**{'status':'fail', 'notification': render_template('_notification.html', text="Sorry, you are not authenticated!")})
        elif current_user.has_role('blocked'):
            return jsonify(**{'status':'fail', 'notification': render_template('_notification.html', text="Sorry, you are in the blacklist!")})





@app.route('/interpreters/<translatorname>', methods=['GET', 'POST'])
def translator(translatorname):
    if request.method == 'GET':
        translator=Translator.query.filter(Translator.slug==translatorname).first()
        user=current_user
        if user.is_authenticated() and not user.has_role('blocked'):
            like = LikeTranslator.query.filter_by(translator=translator, user=user).first()
            if like:
                liked = True
            else:
                liked = False
        else:
            liked = False
        if translator==None:
            abort(404)
        count=len(translator.images)
        posts = PostTranslator.query.filter_by(translator=translator)
        posts = posts.order_by(desc(PostTranslator.date))
        return render_template('translator.html', translator=translator, count=count, already_liked=liked, posts=posts)
    if request.method == 'POST':
        params = request.get_json()
        translator = Translator.query.filter(Translator.slug==params['translator']).first()
        user = current_user
        res = {}

        if params['type'] == 'like':
            if user.is_authenticated() and not user.has_role('blocked'):
                like = LikeTranslator.query.filter_by(translator=translator, user=user).first()
                if like:
                    refuse = True
                    db.session.delete(like)
                else:
                    refuse = False
                    like = LikeTranslator(translator=translator, user=user)
                    db.session.add(like)
                db.session.commit()
            else:
                refuse = True
                if not user.is_authenticated():
                    res['notification'] = render_template('_notification.html', text="Sorry, you are not authenticated!")
                elif user.has_role('blocked'):
                    res['notification'] = render_template('_notification.html', text="Sorry, you are in the blacklist!")
            return jsonify(likes_amount=translator.likes_amount, refuse_like=refuse, **res)

        if params['type'] == 'comment':
            posts = PostTranslator.query.filter_by(translator=translator)
            posts = posts.order_by(desc(PostTranslator.date))
            res = {}

            if user.is_authenticated() and not user.has_role('blocked'):
                #TODO CHECK difference in time
                lastusercomment=posts.filter_by(user=user).first()
                stringcheker=params['text'].replace(' ', '')
                if lastusercomment==None:
                    if stringcheker:
                        #adding new
                        post = PostTranslator(text=params['text'], translator=translator, user=user)
                        db.session.add(post)
                        db.session.commit()
                        res['status']='ok'
                    else:
                        res['notification'] = render_template('_notification.html', text="Please enter some text")

                else:
                    delta=datetime.datetime.now() - lastusercomment.date
                    time_in_seconds=delta.total_seconds()
                    delta=floor(delta.total_seconds() /60)
                    if delta>= 1:
                        if stringcheker:
                            post=PostTranslator(text=params['text'] , translator=translator, user=user)
                            db.session.add(post)
                            db.session.commit()
                            res['status']='ok'
                        else:
                            res['notification'] = render_template('_notification.html', text="Please enter some text")
                    else:
                        time_to_wait=60 - time_in_seconds
                        res['notification'] = render_template('_notification.html', text='Sorry! Wait {0} more seconds'.format(time_to_wait))
                        res['status']='failed'
            else:
                if not user.is_authenticated():
                    res['notification'] = render_template('_notification.html', text="Sorry, you are not authenticated!")
                elif user.has_role('blocked'):
                    res['notification'] = render_template('_notification.html', text="Sorry, you are in the blacklist!")
            comments=translator.comments_amount
            return jsonify(markup=render_template('comment-list.html', posts=posts),comment_amount=comments, **res)