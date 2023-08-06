# -*- coding: utf-8 -*-
# !/usr/bin/env python

import re

from kolibri.stopwords import get_stop_words

stopwords = get_stop_words('en')
stopwords.append('kind')
stopwords.append('many')
stopwords.append('cooperation')
stopwords.append('advance')
import os

filename = os.path.abspath(__file__ + '/../../../../resources/gazetteers/Job_Functions.txt')

functions = open(filename, encoding='utf-8').readlines()

function_re = ''
for funct in functions:
    function_re += funct.strip('\n') + '|'

function_re = function_re[:-1]

function_re = '(?P<signature>(([A-Z][a-z]+\s?)+)?(\s?[\|,]\s?)?({})(.+)?)'.format(function_re)


class EmailMessage(object):
    """
    An email message represents a parsed email body.
    """

    def __init__(self, text):
        self.fragments = []
        self.fragment = None
        self.text = text.replace('\r\n', '\n')
        self.found_visible = False

    def read(self):
        """ Creates new fragment for each line
            and labels as a signature, quote, or hidden.
            Returns EmailMessage instance
        """
        regex = r"(From|To)\s*:[A-Za-z\s\/@\.:,;\&\?\\\(\)'\"\*[\]<>#\/\+-]+?(Subj(ect)?)\s?:|From\s*:[\w @\.:,;\&\(\)'\"\*[\]<>#\/\+-]+?(Sent|Date)\s?:(\s*\d+(\s|\/)(\w+|\d+)(\s|\/)\d+(\s|\/)?(\d+:\d+)?)?|From\s*:[\w @\.:,;\&\(\)'\"\*[\]<>#\/\+-]+?(Sent\s+at)\s?:(\s*\d+\s\w+\s\d+\s?\d+:\d+)?|From\s*:[\w @\.:,;\&\?\\\(\)'\"\*[\]<>#\/\+-]+?(CC)\s?:|From\s*:[\w @\.:,;\&\?\\\(\)'\"\*[\]<>#\/\+-]+?(To)\s?:"

        starts = [m.start(0) for m in re.finditer(regex, self.text, re.MULTILINE | re.UNICODE)]

        if len(starts) < 1:
            self.fragments.append(Fragment(self.text))

        else:
            if starts[0] > 0:
                starts.insert(0, 0)
            lines = [self.text[i:j] for i, j in zip(starts, starts[1:] + [None])]

            for line in lines:
                self.fragments.append(Fragment(line))

        return self


class Fragment(object):
    """ A Fragment is a part of
        an Email Message, labeling each part.
    """

    def __init__(self, email_text):

        self.body = email_text.strip()
        self.is_forwarded_message = self._get_forwarded()
        self.headers = self._get_header()
        self.attachement = self._get_attachement()
        self.salutation = self._get_salutation()
        self.disclaimer = self._get_disclaimer()
        self.signature = self._get_signature()

        self._content = email_text

    def _get_attachement(self):
        pattern = r'(?P<attachement>(^\s*[a-zA-Z0-9_,\. -]+\.(png|jpeg|docx|doc|xlsx|xls|pdf|pptx|ppt))|Attachments\s?:\s?([a-zA-Z0-9_,\. -]+\.(png|jpeg|docx|doc|xlsx|xls|pdf|pptx|ppt)))'
        groups = re.search(pattern, self.body, re.IGNORECASE)
        attachement = ''
        if not groups is None:
            if "attachement" in groups.groupdict().keys():
                attachement = groups.groupdict()["attachement"]
                self.body = self.body[len(attachement):].strip()
        return attachement

    def _get_salutation(self):
        # Notes on regex:
        # Max of 5 words succeeding first Hi/To etc, otherwise is probably an entire sentence
        salutation_opening_statements = [
            "hi",
            "dear",
            "to",
            "hey",
            "hello",
            "thanks",
            "All",
            "good morning",
            "good afternoon",
            "good evening"]

        pattern = r'(?P<salutation>(^(- |\s)*\b(' + r'|'.join(
            salutation_opening_statements) + r')\b' + r'((\s*\w+){0,2}\s*,|([A-Z]\w+)|)))'

        groups = re.match(pattern, self.body, re.IGNORECASE)
        salutation = ''
        if groups is not None:
            if "salutation" in groups.groupdict().keys():
                salutation = groups.groupdict()["salutation"]
                self.body = self.body[len(salutation):].strip()
        return salutation

    def _get_header(self):
        regex = r"From\s*:[\w @\.:,;\&\?\\\(\)'\"\*[\]<>#\/\+-]+?(Subj(ect)?)\s?:|From\s*:[\w @\.:,;\&\(\)'\"\*[\]<>#\/\+-]+?(Sent|Date)\s?:(\s*\d+(\s|\/)(\w+|\d+)(\s|\/)\d+(\s|\/)?(\d+:\d+)?)?|From\s*:[\w @\.:,;\&\(\)'\"\*[\]<>#\/\+-]+?(Sent\s+at)\s?:(\s*\d+\s\w+\s\d+\s?\d+:\d+)?|From\s*:[\w @\.:,;\&\?\\\(\)'\"\*[\]<>#\/\+-]+?(CC)\s?:|From\s*:[\w @\.:,;\&\?\\\(\)'\"\*[\]<>#\/\+-]+?(To)\s?:"

        pattern = r"(?P<header_text>(" + regex + "))"

        groups = re.search(pattern, self.body, + re.DOTALL)
        header_text = None
        if groups is not None:
            if "header_text" in groups.groupdict().keys():
                header_text = groups.groupdict()["header_text"]
                self.body = self.body[len(header_text):].strip()
        return header_text

    def _get_disclaimer(self):
        disclaimer_openings = [
            "\*+CLASSIFIED PERSONNEL INFORMATION\*+",
            "\*+Confidentiality Notice\*+",
            "Confidentiality Notice - This email transmission and any documents",
            "ATTENTION: The information in this e-mail is confidential",
            "Because email is not secure, we strongly recommend",
            "CLASSIFIED PERSONNEL INFORMATION",
            "CONFIDENTIAL NOTICE:",
            "Confidentiality Notice\s*:",
            "CONFIDENTIALITY NOTICE\s*:?",
            "CONFIDENTIALITY: This email is intended",
            "Disclaimer: This email and its content are confidential",
            "DISCLAIMER:",
            "Document from Retirement Corporation of America",
            "GOGREEN",
            "Go green",
            "This email is classified as Limited Access",
            "LEGAL NOTICE\s*Unless expressly stated otherwise",
            "Going Green: Please consider the environment ",
            "his message may contain information that is confidential",
            "If you have any pending questions please reply to this message",
            "IMPORTANT NOTICE:\s*This email and any attachments",
            "IMPORTANT NOTICE: This email is confidential",
            "IMPORTANT NOTICE: Please note that this Webex service allows",
            "IMPORTANT - PLEASE READ: This electronic message, including its attachments",
            "Information in this message is confidential",
            "Information on this e-mail is confidential",
            "NA: This is an automated email notification",
            "Notice of Confidentiality",
            "NOTICE OF CONFIDENTIALITY\s*:",
            "This electronic message \(including any attachments\)",
            "NOTICE: The information contained in this electronic mail",
            "NOTE: This message or its attachments may give you access to sensitive personal",
            "NOTICE: This electronic mail message and any attached files are confidential",
            "Please also use our Recruitment Toolkit which is there for your support 24 hours a day",
            "NOTICE:\s+This e-mail may contain confidential information",
            "Please consider the environment before printing this e-mail",
            "Please consider the environment before printing this email",
            "Please do not share this email",
            "PRIVATE & CONFIDENTIAL",
            "Protect our environment - please only print this if you have to",
            "The information contained in this communication",
            "The\s+information\s+contained\s+in\s+this\s+electronic\s+message",
            "The information contained in this email",
            "The content of this email is confidential",
            "The information contained in this message",
            "The information in this e-mail and any attachment",
            "Important: This\s+employee-mail is intended for the above named only",
            "This  employee-mail and its attachments are intended for the above named recipient",
            "This\s+employee-mail transmission contains ",
            "This communication is intended for the use of the addressee only",
            "This\s+employee-mail message is confidential",
            "This\s+employee-mail may contain confidential",
            "This  employee-mail message, including any attachments",
            "This  employee-mail may contain confidential",
            "This communication may contain information that is proprietary",
            "This communication contains information that is confidential",
            "This communication contains information that may be confidential",
            "This communication may contain information that is legally proprietary",
            "The contents of this email and any attachments are confidential",
            "This e-mail \(including any attachments\)",
            "This E-Mail is confidential",
            "This e-mail is intended solely for the addressee",
            "This e-mail transmission contains information that is confidential",
            "This email \(and any attachments\) may contain",
            "This e-mail \(and any attachments\) is confidential",
            "This email and any attachments are confidential",
            "This email and any files attached are confidential",
            "This email contains confidential material prepared for the intended addressees",
            "This email contains proprietary and confidential",
            "Confidentiality Statement and Disclaimer",
            "Disclaimer: The information contained in this e-mail message",
            "This e-mail \(including any attachments\) is intended for the addressee",
            "This email, including any attachments, is confidential",
            "This email is confidential and ",
            "In summary: This email and attachments may be confidential",
            "This email is sent on behalf of ",
            "This message contains proprietary information from Equifax",
            "This email may contain legally privileged, confidential information",
            "This email may contain proprietary and confidential material",
            "This email message, including any attachments, contains or may contain confidential",
            "This message \(including any attachments\)",
            "This message and any attached documents",
            "This message and the information contained in or attached to it are private",
            "This message and its attachments \(if any\) may contain confidential",
            "This email message and its attachments are for the sole use of the intended recipient",
            "This message is for the designated recipient only",
            "This message is intended for the use of the addressee and may contain",
            "This message may contain information that is confidential",
            "This message may contain confidential",
            "This message is from DHL Supply Chain and may contain confidential business information",
            "This transmission is intended only for use by the intended recipient",
            "This transmission was generated by our rate program and automatically forwarded to your attention",
            "ThyssenKrupp Presta message disclaimer:",
            "Click this link to go directly to",
            "This e-mail is for the intended recipient only",
            "If you  are not the intended recipient of this mail,",
            "If you received this transmission in error, please advise the sender",
            "If the reader of this message, regardless of the address or routing, is not an intended recipient",
            "You are being sent this mail as your email address is recorded in our",
            "This communication and its attachments, if any, may contain confidential",
            "Thank you for considering the environmental impact of printing emails",
            "CAUTION - This message may contain privileged",
            "THIS ELECTRONIC MESSAGE, INCLUDING ANY ACCOMPANYING DOCUMENTS",
            "Please go to\s*https://ows01.hireright.com",
            "To view this screening report(.|\n)*HireRight website\.",
            "For more information on Xerox products and solutions, please visit",
            "This email is sent on behalf of Northgate Information Solutions Limited and its associated companies",
            "BE AWARE OF WIRE SCAM\s*(\!)* - Recently the mortgage industry received",
            "IMPORTANT: PRIVATE COMMUNICATION TO DESIGNATED RECIPIENT \(S\) ONLY"
        ]

        pattern = r"\s*(?P<disclaimer_text>(" + "|".join(disclaimer_openings) + ")(\s*\w*))"

        groups = re.search(pattern, self.body, re.MULTILINE)
        disclaimer_text = None
        if groups is not None:
            if "disclaimer_text" in groups.groupdict().keys():
                found = groups.groupdict()["disclaimer_text"]
                disclaimer_text = self.body[self.body.find(found):]
                self.body = self.body[:self.body.find(disclaimer_text)].strip()

        return disclaimer_text

    def _get_signature(self):
        # note - these openinged statements *must* be in lower case for
        # sig within sig searching to work later in this func

        # TODO DRY

        sig_opening_statements_small = [
            "many thanks",
            "thanks",
            "Thanks",
            "sincerely",
            "ciao",
            "Best wishes",
            "Best regards",
            "Kind regards",
            "Regards",
            "Best",
            "bGIF",
            "Dank alvast",
            "thankyou",
            "thank you",
            "talk soon",
            "cordially",
            "Respectfully",
            "yours truly",
            "thanking You",
            "Mit freundlichen"
        ]
        sig_opening_statements = [
            "warm regards",
            "With kind regards",
            "Thanks in advance",
            "kind regards",
            "have a great afternoon",
            "Best Regards,",
            "Danke und VG",
            "thank you",
            "Thanks and Regards",
            "Thanks & Regards",
            "Thanks & Regards,",
            "Thank you\.",
            "Thank you,",
            "Gracias",
            "regards",
            "Sincères Amitiés",
            "regards\.",
            "Mit freundlichem",
            "With best wishes",
            "Med vänlig hälsning",
            "cheers",
            "many thanks",
            "thanks",
            "Thanks",
            "Dank alvast",
            "sincerely",
            "ciao",
            "All the best",
            "bGIF",
            "Best.",
            "Best,",
            "Thx in advance",
            "Viele Grüße",
            "Vielen Dank",
            "cordialmente saluto",
            "Thank you(?!\sfor)",
            "thankyou",
            "Much appreciated,",
            "talk soon",
            "cordially",
            "Pozdrawiam",
            "Fax Reception Report  Received Time",
            "yours truly",
            "thanking You",
            "Mit freundlichen",
            "Meilleures salutations",
            "sent from my iphone",
            "To print the report:"]
        pattern = r'(?P<signature>(' + '|'.join(sig_opening_statements) + ')(.)*)'
        pattern2 = r'(?P<signature>(' + '|'.join(sig_opening_statements_small) + ')(.)*)'

        groups = re.search(pattern, self.body, re.IGNORECASE + re.DOTALL)
        signature = None
        if groups:
            if "signature" in groups.groupdict().keys():
                signature1 = groups.groupdict()["signature"]
                # search for a sig within current sig to lessen chance of accidentally stealing words from body
                tmp_sig = signature1
                for s in sig_opening_statements_small:
                    if tmp_sig.lower().find(s) == 0:
                        tmp_sig = tmp_sig[len(s):]
                groups = re.search(pattern2, tmp_sig, re.IGNORECASE + re.DOTALL)
                remaing = ""
                signature2 = ""
                if groups:
                    signature2 = groups.groupdict()["signature"]
                    remaing = tmp_sig[:tmp_sig.find(signature2)].lower().replace(',', '').replace('-', '')
                    for statement in sig_opening_statements:
                        remaing = remaing.replace(statement.lower(), '')
                    for stp in stopwords:
                        remaing = re.sub(r'\b' + stp + r'\b', '', remaing)
                if len(remaing.strip().split()) > 1:
                    signature = signature2
                else:
                    signature = signature1
                self.body = self.body[:self.body.find(signature)].strip()
        else:
            groups = re.search(function_re, self.body, re.DOTALL)

            if groups is not None and "signature" in groups.groupdict().keys():
                signature = groups.groupdict()["signature"]
                # search for a sig within current sig to lessen chance of accidentally stealing words from body
                tmp_sig = signature
                for s in sig_opening_statements_small:
                    if tmp_sig.lower().find(s) == 0:
                        tmp_sig = tmp_sig[len(s):]
                groups = re.search(pattern2, tmp_sig, re.IGNORECASE + re.DOTALL)
                if groups:
                    signature = groups.groupdict()["signature"]
                self.body = self.body[:self.body.find(signature)].strip()
        return signature

    def _get_forwarded(self):

        pattern = '(?P<forward_text>([- ]* Forwarded Message [- ]*|[- ]* Forwarded By [- ]*|[- ]*Original Message[- ]*))'
        groups = re.search(pattern, self.body, re.DOTALL)
        forward = None
        if groups is not None:
            if "forward_text" in groups.groupdict().keys():
                forward = groups.groupdict()["forward_text"]

        if forward is not None:
            self.body = self.body.replace(forward, '')

        return forward is not None

    @property
    def content(self):
        return self._content.strip()
