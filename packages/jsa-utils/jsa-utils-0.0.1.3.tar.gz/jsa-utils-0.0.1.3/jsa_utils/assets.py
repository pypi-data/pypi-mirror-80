import json
import datetime
import pika
import pdfkit
from random import randint

from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.core.mail import get_connection


def compile_form_errors(form):
    field_errors = []
    count = 1
    for field in form:
        for error in field.errors:
            field_errors.append({"field": field.name, "error": error})
            count = count + 1

    return field_errors


def compile_validation_errors(form, resp):
    errors = []
    for err in form.errors["__all__"]:
        print(err)
        errors.append(err)
    resp.add_message("{}".format(",".join(errors)))


def get_modifier(mod_string):

    # Numeric modifiers
    if str(mod_string).upper() == "EQ" or str(mod_string).upper() == "":
        return ""
    elif str(mod_string).upper() == "GT":
        return "gt"
    elif str(mod_string).upper() == "LT":
        return "lt"
    elif str(mod_string).upper() == "GTE":
        return "gte"
    elif str(mod_string).upper() == "LTE":
        return "lte"
    # String modifiers
    elif str(mod_string).upper() == "LK":
        return "icontains"
    elif str(mod_string).upper() == "SW":
        return "istartswith"
    elif str(mod_string).upper() == "EW":
        return "iendswith"

    return ""


def build_query_filter(filter_array=None):

    kwargs = dict()
    kwargs["active"] = True

    for _filter in filter_array:
        modifier = get_modifier(_filter.get("modifier", ""))
        if modifier == "":
            if (
                _filter.get("field", None) is not None
                and _filter.get("value", None) is not None
            ):
                kwargs[_filter.get("field")] = _filter.get("value")
        else:
            if (
                _filter.get("field", None) is not None
                and _filter.get("value", None) is not None
            ):
                fld = _filter.get("field")
                kwargs["{0}__{1}".format(fld, modifier)] = _filter.get("value")

    return kwargs


def build_query_sorter(sort_obj=None):
    pass


def build_pagination_markers(page_num=1, page_size=10):

    if page_num and page_size:
        lower_mark = (int(page_num) - 1) * int(page_size)
        upper_mark = int(page_num) * int(page_size)

        pager = {"lm": lower_mark, "um": upper_mark}

    return pager


def get_contents(request):
    contents = None

    if request.method == "POST":
        param_dict = request.POST.dict()
        if contents is None and param_dict:
            contents = param_dict

    if contents is None:
        param_dict = request.GET.dict()
        if contents is None and param_dict:
            contents = param_dict

    if contents is None:
        try:
            if request.body is not None:
                print("--- Reading from Json Body--")
                try:
                    print("-- Request Body--", request.body)
                    contents = json.loads(request.body.decode("utf-8"))
                except Exception as err:
                    print("--Exception thrown --", err)
                    contents = None
        except Exception as err:
            print("--Exception thrown --", err)
            contents = None

    print("--Extracted Contents--", contents)

    return contents


def generate_serial_number(size=4):

    # Append last random four
    code_num = ""
    for _ in range(size):
        value = randint(0, 9)
        code_num = code_num + str(value)

    return code_num


def generate_client_location_code(
    client_prefix=None, location=""
):  # abstracted from generate_party_code
    code = ""
    if client_prefix:
        code = client_prefix + location

        # Append current date
        # code = code+str(datetime.date.today().strftime("%y"))+str(datetime.date.today().month)+str(datetime.date.today().day)
        code = code + str(datetime.date.today().strftime("%y"))

        # Append last random four
        code_num = ""
        for _ in range(4):
            value = randint(0, 9)
            code_num = code_num + str(value)

        code = code + "" + code_num

    return code


def get_broker_channel():
    """
    Expects the values to be made available in settings file
    BROKER_CONNECTION OR (MESSAGING_USERNAME, MESSAGING_PWORD, BROKER_IP, BROKER_PORT, BROKER_VHOST)

    :return: broker_channel
    """
    try:
        if settings.BROKER_CONNECTION is None:
            print("---> Establishing broker connection & channel")
            creds = pika.PlainCredentials(
                settings.MESSAGING_USERNAME, settings.MESSAGING_PWORD
            )
            params = pika.ConnectionParameters(
                settings.BROKER_IP, settings.BROKER_PORT, settings.BROKER_VHOST, creds
            )
            BROKER_CONNECTION = pika.BlockingConnection(params)
            broker_channel = BROKER_CONNECTION.channel()

        else:
            broker_channel = settings.BROKER_CONNECTION.channel()

    except Exception as err:
        print(">> EXCEPTION: ", str(err))

    return broker_channel


def publish_event_topic(topic=None, payload={}):
    """
    This function posts messages to the Jetstream Topic exchange

    :param topic: The topic of the message for the purpose of routing
    :param payload: Message payload to be received by each topic subscriber
    :return:
    """
    channel = get_broker_channel()
    if channel:
        props = pika.BasicProperties(content_type="application/json")
        channel.basic_publish(
            exchange="JETSTREAM_TX",
            routing_key=topic,
            body=json.dumps(payload),
            properties=props,
        )

    channel.close()


def publish_event_broadcast(payload={}):
    pass


def publish_direct_message(queue=None, payload={}):
    pass


def send_email_notification(
    to_address,
    from_address,
    subject="Notification",
    contxt=None,
    email_template=None,
    attachment=None,
    bcc_lst=None,
):
    if contxt is not None and email_template is not None:

        print(
            "------->>>>>>> Executing task - Sending Email Notification <<<<---------- "
        )
        print("%s" % contxt)
        print(
            "--------------------------------------------------------------------------"
        )
        try:
            # Prepare Email message parts.
            body = get_template(email_template)
            email = EmailMessage()
            email.subject = subject
            email.from_email = from_address
            email.to = to_address
            email.connection = get_connection()
            email.body = body.render(contxt)
            email.content_subtype = "html"
            if attachment is not None:
                email.attach(attachment[0], attachment[1], attachment[2])

            if bcc_lst is not None:
                email.bcc = bcc_lst

            email.send()

        except Exception as err:
            print("++++++++++++ Email Notification task failed - [ %s ] " % (err))


def render_to_pdf(html_doc=None, filename="-"):
    print("=== Rendering to PDF <<====")
    pdf_file = None

    if html_doc:
        try:
            doc = pdfkit.from_string(html_doc, filename)
            if doc:
                print("===>> Generated PDF Correctly <<===")
                pdf_file = open(filename, "rb")

        except Exception as err:
            print("===>> Error: {}".format(err))

        return pdf_file

    else:
        return pdf_file
