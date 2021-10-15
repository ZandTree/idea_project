LOGGING = {
    'version': 1,
    # let op: when too set it to True
    # let the dafault loggers(ORM,db ect) be
    'disable_existing_loggers': False,
    'formatters':{
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },        
    },
    'handlers': { 
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter':'simple'
        },
        'dj': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter':'verbose',                     
            'maxBytes':1024*1024*1,#1MB
            'backupCount':5,
            'filename':'logs/django_native.log',
        },
        'upload_problems': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes':1024*1024*1,
            'backupCount':5,
            'formatter':'verbose',
            'filename':'logs/upload.log',
        },
        'users': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes':1024*1024*1,
            'backupCount':5,
            'formatter':'verbose',
            'filename':'logs/user_issues.log',
        },
        'mail_admin':{
            'level':'CRITICAL',            
            'class':'django.utils.log.AdminEmailHandler',
            # if != default see above 'email_backend': 'django.core.mail.backends.filebased.EmailBackend',            
        }       
    },
    'loggers': {
        'django': {
            'handlers': ['dj','console'],
            # 'handlers': ['mail_admin','dj'],
            'level': 'WARNING',
            'propagate': False,
        },        
        'upload':{
            'handlers':['upload_problems'],
            'level':'WARNING',      
        },     
        'user_issues':{
            'handlers':['users'],
            'level':'INFO',      
        },
            
    }
}
