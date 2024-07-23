# html_template.py: Script para criar os templates de HTML para a interface do chatbot Aila

hide_st_style = '''
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
'''

css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #eb9947;
    justify-content: flex-end;
    flex-direction: row-reverse;
}
.chat-message.bot {
    background-color: #e66b19;
    justify-content: flex-start;
    flex-direction: row;
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 86px;
  max-height: 86px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
'''

ai_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.ibb.co/JdjgxHL/ai-profile-photo.png">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

human_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://i.ibb.co/nRsvtWs/human-profile-photo.png">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''