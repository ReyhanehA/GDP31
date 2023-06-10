from django import template
from django.utils.safestring import mark_safe

from omblog.forms import CreatePostForm
register = template.Library()


@register.inclusion_tag('omblog/_create_form.html', takes_context=True)
def create_form(context):
    return{
        'form': CreatePostForm(),
        'context': context}


class VerbatimNode(template.Node):

    def __init__(self, text):
        self.text = text

    def render(self, context):
        return self.text


@register.tag
def verbatim(parser, token):
    text = []
    while 1:
        token = parser.tokens.pop(0)
        if token.contents == 'endverbatim':
            break
        if token.token_type == template.TOKEN_VAR:
            text.append('{{')
        elif token.token_type == template.TOKEN_BLOCK:
            text.append('{%')
        text.append(token.contents)
        if token.token_type == template.TOKEN_VAR:
            text.append('}}')
        elif token.token_type == template.TOKEN_BLOCK:
            text.append('%}')
    return VerbatimNode(''.join(text))


class VideoNode(template.Node):

    def __init__(self, h264, webm, poster):
        self.h264 = h264
        self.webm = webm
        self.poster = poster

    def render(self, context):
        context = {
            'webm': self.webm,
            'h264': self.h264,
            'poster': self.poster
        }
        html = """<video controls="controls" poster="%(poster)s" preload>
<source src="%(h264)s" type='video/mp4; codecs="avc1.42E01E,mp4a.40.2"'>
<source src="%(webm)s"  type='video/webm; codecs="vp8, vorbis"'>
<object id="flashvideo" width="720" height="540"
data="http://releases.flowplayer.org/swf/flowplayer-3.2.10.swf"
type="application/x-shockwave-flash">
<param name="movie"
value="http://releases.flowplayer.org/swf/flowplayer-3.2.10.swf">
<param name="allowfullscreen" value="true">
<param name="allowscriptaccess" value="always">
<param name="flashvars" value='config={"clip":{"url":"%(h264)s}}'>
</object>
</video>""" % context
        return mark_safe(html)


@register.tag
def video(parser, token):
    bits = token.contents.split()
    return VideoNode(bits[1], bits[2], bits[3])


@register.simple_tag
def post_status(post):
    return post.get_status_display().lower()
