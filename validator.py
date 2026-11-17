import re

class Validator:
    def validate_username(self, username):
        err_msg = []
        pattern = r"[_0-9A-Za-z]+"
        if len(username) < 4:
            err_msg.append("Username must have Minimum 4 characters")
        if len(username) > 20:
            err_msg.append("Username must have Maximum 20 characters.")
        if not re.fullmatch(pattern, username):
            err_msg.append("Only letters, digits and underscores are allowed.")
        return err_msg
            
    def validate_password(self, password):
        err_msg = []
        pattern = r"[@#$!]"
        if len(password) < 8:
            err_msg.append("The Password must have Minimum 8 characters.")
        if not any(char.isupper() for char in password):
            err_msg.append("The Password must have At least one uppercase letter (A-Z)")
        if not any(char.isdigit() for char in password):
            err_msg.append("The Password must have At least one digit (0-9).")
        if not re.search(pattern, password):
            err_msg.append("The Password must have At least one special character (@, #, $, !, etc.).")
        return err_msg
    
    def validate_email(self, email):
        err_msg = []
        addExist = email.find("@")
        dotExist = email.find(".")
        if addExist < 0:
            err_msg.append("Email must have @")
        if dotExist < 0 :
            err_msg.append("Email must have '.'")
        if addExist >= 0 and dotExist >= 0:
            if addExist > dotExist:
                err_msg.append(". must appear after @")
        return err_msg
    
