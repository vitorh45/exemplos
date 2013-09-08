from django import template
from polls.models import Poll

register = template.Library()

def percent(value,arg):
    total_votes = 0
    for choice in arg:
        total_votes += choice.votes
    percent_value = (100*value)/total_votes
    return percent_value

def do_get_poll(parser, token):
    bits = token.split_contents()
    if len(bits) != 3:
        raise template.TemplateSyntaxError("'get_poll' tag takes exactly 3 arguments")
    return PollNode(bits[2])

class PollNode(template.Node):
    def __init__(self, varname):
        self.varname = varname
    def render(self, context):
        try:
            poll = Poll.objects.filter(is_active=True)[0]
        except:
            poll = None
        context[self.varname] = poll
        return ''

def do_get_total_votes(parser, token):
    bits = token.split_contents()
    if len(bits) != 4:
        raise template.TemplateSyntaxError("'get_total_votes' tag takes exactly 4 arguments")
    return TotalVotesNode(bits[2],bits[3])

class TotalVotesNode(template.Node):
    def __init__(self, varname, poll_id):
        self.varname = varname
        self.poll_id = template.Variable(poll_id)
    def render(self, context):
        poll_id = self.poll_id.resolve(context)
        try:
            poll = Poll.objects.get(id=poll_id)
        except:
            poll = None
            context[self.varname] = poll
            return ''
        votes = 0
        for choice in poll.choice_set.all():
            votes += choice.votes
        context[self.varname] = votes
        return ''

register.filter('percent', percent)
register.tag('get_poll', do_get_poll)
register.tag('get_total_votes', do_get_total_votes)

