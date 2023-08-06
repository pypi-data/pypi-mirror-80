from ipywidgets import widgets,interact, Layout
import rwth_nb.plots.colors as rwthcolors
rwth_colors = rwthcolors.rwth_colors

import datetime
import json
import os
import hashlib # for anonymizing the username

def get_notebook_name():
    try:
        # import necessary packages (see https://github.com/jupyter/notebook/issues/1000)
        # importing inside function because those libraries should only be included if they are realy needed
        import json
        import re
        import ipykernel
        import requests
        import os

        from requests.compat import urljoin
        from notebook.notebookapp import list_running_servers

        # now determine calling notebook name
        kernel_id = re.search('kernel-(.*).json',
                              ipykernel.connect.get_connection_file()).group(1)
        servers = list_running_servers()
        for ss in servers:
            response = requests.get(urljoin(ss['url'], 'api/sessions'),
                                    params={'token': ss.get('token', '')})
            for nn in json.loads(response.text):
                if nn['kernel']['id'] == kernel_id:
                    relative_path = nn['notebook']['path']
                    return os.path.splitext(os.path.split(os.path.join(ss['notebook_dir'], relative_path))[1])[0]
    except:
        return 'tmp'


def rwth_feedback(feedback_name, questions, feedback_path='feedback.json', mail_to=None, mail_from='feedback@jupyter.rwth-aachen.de', mail_subject=None, mail_smtp_host='smarthost.rwth-aachen.de'):
    global widgets_container
    is_feedback_edited = is_send_confirmed = False

    def on_feedback_edited(_):
        nonlocal is_feedback_edited
        is_feedback_edited = True

    # Internationalization
    feedback_scale_options_de = ['Stimme voll zu', 'Ich stimme zu', 'Keine Meinung', 'Ich stimme nicht zu', 'Ich stimme gar nicht zu'] # Likert-scale
    feedback_text_de = {"your-feedback" : "Dein Feedback ...",
                    "send" : "Absenden",
                    "confirm_send" : "Zum Absenden bitte bestätigen.",
                    "sent" : "Dein Feedback wurde abgeschickt. Vielen Dank!",
                    "empty" : "Bitte geben Sie zuerst Feedback ein, das abgesendet werden kann.",
                    "mailfailure": "Die Mail mit dem Feedback konnte nicht versendet werden. Das Feedback wurde lokal abgespeichert."}
    # TODO: Add at least English here
    
    # Select language
    feedback_scale_options = feedback_scale_options_de; feedback_text = feedback_text_de;
    
    # Default arguments for toggle_button and textarea
    toggle_args = {"options" : feedback_scale_options, 
                   "index" : 2,  "description" : "",  "disabled" : False,  "style": {'button_color': rwth_colors['rwth:green-50']},  "tooltips" : []}
    textarea_args = {"value" : "",  "placeholder" : feedback_text['your-feedback'], 
                     "description" : "",  "disabled" : False}
    
    widgets_container = [];
    widgets_values = [];
    for question in questions:
        if question['type'] == 'free-text':
             # Free text
            widget_label = widgets.HTML(value="<b>{}</b>".format(question['label']))
            widget_value = widgets.Textarea(**textarea_args)
            widget_value.observe(on_feedback_edited, 'value')
                        
        elif question['type'] == 'scale':
            # Toggle Buttons
            widget_label = widgets.HTML(value="<b>{}</b>".format(question['label']))
            widget_value = widgets.ToggleButtons(**toggle_args)
            widget_value.observe(on_feedback_edited, 'value')

        widgets_container.append(widget_label)
        widgets_container.append(widget_value)
        widgets_values.append(widget_value) # TODO: Get rid of this?

    # Button 
    button = widgets.Button(description = feedback_text['send'], disabled = False, style= {'button_color': rwth_colors['rwth:green-50'], 'margin':'10px'}, icon='', layout=Layout(margin='20px 0 0 0'))
    output = widgets.Output()
    
    # Button click callback
    def on_button_clicked(b):
        nonlocal is_send_confirmed

        if not button.disabled:
            entry = {}

            nonlocal is_feedback_edited
            if not is_feedback_edited:
                with output:
                    print(feedback_text['empty'])    
            else:
                # set up json entries
                entry['name'] = feedback_name
                entry['date'] = "{}".format(datetime.datetime.now())
                if 'USER' in os.environ.keys():
                    user_name = os.environ['USER']
                else:
                    user_name = os.environ['HOSTNAME']  # take hostname as fall-back
                entry['userhash'] = hashlib.sha256(str.encode(user_name)).hexdigest()
                entry['answer'] = {q['id']: v.value for q, v in zip(questions, widgets_values)}

                if not is_send_confirmed:
                    button.description = feedback_text['confirm_send']
                    button.layout.width = 'auto'
                    is_send_confirmed = True
                    return

                # dump entries into json file
                if not os.path.isfile(feedback_path):
                    with open(feedback_path, mode='w', encoding='utf-8') as f:
                        json.dump([], f)
                with open(feedback_path, mode='r', encoding='utf-8') as f:
                    entries = json.load(f)
                with open(feedback_path, mode='w', encoding='utf-8') as f:
                    entries.append(entry)
                    json.dump(entries, f)

                # send json file as attachment of mail
                if mail_to is not None:
                    try:
                        import smtplib
                        from email.mime.multipart import MIMEMultipart
                        from email.mime.base import MIMEBase
                        from email import encoders
                        
                        # create message                
                        msg = MIMEMultipart()
                        msg['From'] = mail_from
                        msg['To'] = mail_to
                        
                        if mail_subject is not None:
                            msg['Subject'] = mail_subject
                        else:
                            msg['Subject'] = feedback_name

                        # open the file to be sent as attachment
                        with open(feedback_path, 'rb') as attachment:
                            # attach file to mail
                            p = MIMEBase('application', 'octet-stream')
                            p.set_payload(attachment.read())

                        # encode and add as attachment to message
                        encoders.encode_base64(p)
                        p.add_header('Content-Disposition', "attachment; filename= %s" % feedback_path)
                        msg.attach(p)

                        # send mail
                        s = smtplib.SMTP(mail_smtp_host)
                        text = msg.as_string()
                        s.sendmail(mail_from, mail_to, text)

                        # close connection
                        s.quit()

                        with output:
                            print(feedback_text['sent'])

                    except ConnectionRefusedError:
                        # Not connected to the RWTH network
                        with output:
                            print(feedback_text['mailfailure'])

                button.disabled = True

    # Set callback to button
    button.on_click(on_button_clicked)

    # Display widgets
    display(widgets.VBox(widgets_container), 
        button, output)