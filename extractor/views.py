from os import listdir
from os.path import isfile, join

from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from pyspark import SparkContext, SparkConf

from extractor.forms import FileUrlForm
from functions.headers import get_headers

from extractor.filter import functions as filter_functions


def index(request):
    template = loader.get_template('extractor/index.html')
    context = {}

    if request.method == 'POST':
        form = FileUrlForm(request.POST)
        if form.is_valid():
            selected_file = request.POST['selected_file']
            request.session['datafile'] = './data/' + selected_file
            return redirect('/file')

    else:
        form = FileUrlForm()
        files = [f for f in listdir('./data/') if isfile(join('./data/', f))]
        context['files'] = files

    context['form'] = form
    return HttpResponse(template.render(context, request))


def file(request):
    datafile = request.session['datafile']
    sc = SparkContext(conf=SparkConf().setAppName("data").setMaster("local[2]"))
    data_text_file = sc.textFile(datafile)
    headers, header_types = get_headers(data_text_file)

    count = data_text_file.count() - 1
    sc.stop()

    context = {
        'file_headers': headers,
        'file_header_types': header_types,
        'count': count
    }

    template = loader.get_template('extractor/file.html')
    return HttpResponse(template.render(context, request))


def filter_data_file(datafile, header, header_type, filter_value, condition):
    sc = SparkContext(conf=SparkConf().setAppName("data").setMaster("local[2]"))

    filter_method = filter_functions.get_filter_method(header_type, condition)

    try:
        data_text_file = sc.textFile(datafile)
        headers, header_types = get_headers(data_text_file)
        result = data_text_file.filter(lambda line: line != header) \
            .map(lambda line: line.split(",")) \
            .filter(lambda line: len(line) > header) \
            .filter(lambda line: filter_method(line[header], filter_value)) \
            .count()
        sc.stop()
    except Exception:
        sc.stop()

    return headers, header_types, result


def filter(request):
    filter_value = request.POST['filter_value']
    count = request.POST['count_hidden']

    header = int(request.POST['form_control_headers_select'])
    datafile = request.session['datafile']

    header_type = str(request.POST['type_hidden'])
    if header_type == 'number':
        condition = str(request.POST['form_control_headers_number_condition'])
    elif header_type == 'string':
        condition = str(request.POST['form_control_headers_string_condition'])

    headers, header_types, result = filter_data_file(datafile, header, header_type, filter_value, condition)

    context = {
        'file_headers': headers,
        'file_header_types': header_types,
        'count': count,
        'result': result
    }

    template = loader.get_template('extractor/file.html')
    return HttpResponse(template.render(context, request))
