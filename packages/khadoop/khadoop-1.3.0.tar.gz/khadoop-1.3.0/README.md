# README

Parse and slice hadoop logs

## Yarn RM

![alt](img/yarn-rm.png)

### Dataset

```python
from khadoop.yarn import logrm
```

Parse all files that look like a regular Ressource Manager log with default name.

`logrm.FILEPATTERN` is a unix-like pattern file to help glob them.

```python
parsed = []
for filelog in LOGFOLDER.glob(logrm.FILEPATTERN):
    print(filelog)
    parsed += logrm.process(filelog.open())
```

`logrm.process` will parse each line and produce a list of dict with sensible information

each dict look like :

```python
 {
   'accepted_to_running': 6,  # nb sec between ACCEPT to RUNNING
   'id_application': 'application_1596547077642_6854',
   'accept_to_running_ts':'2020-08-06 14:59:59,119' # timestamp set for log line 'FROM accepted to RUNNING'
   }
```

the `accepted_to_running` represent here the number between these two timestamps on yarn aggregated RM log:

```log
2020-08-06 14:59:52,756 INFO  rmapp.RMAppImpl (RMAppImpl.java:handle(779)) - application_1596547077642_6854 State change from SUBMITTED to ACCEPTED
...
2020-08-06 14:59:59,119 INFO  rmapp.RMAppImpl (RMAppImpl.java:handle(779)) - application_1596547077642_6854 State change from ACCEPTED to RUNNING
```

## Related

- https://github.com/etsy/logster
