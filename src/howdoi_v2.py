import sublime, sublime_plugin, subprocess
import logging
import sys
import urllib.parse


USER_PATH="/Users/XXXXX/"


BING_PYTHON_EXEC_PATH= USER_PATH +  "/conda3/miniconda3/envs/py38ab/bin/python "

BINGCHAT_PATH        = USER_PATH +   '/D/gitdev/aamL_devctr1/mlc/ztmp/bbing/'

BINGCHAT_CMD         = BINGCHAT_PATH + "/cchat.py run_chat" 




class HowdoiDirectCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
                line = self.view.line(region)
                cont = self.view.substr(line)


                cont = cont.strip()
                if (len(cont)<1): continue

                first_word = cont.split(" ")[0]
                # logging.debug('First word: ' + first_word)

                if first_word in ['google',  'gg' ]:
                    query = urllib.parse.quote_plus(' '.join(cont.split(" ")[1:]))
                    url   = '"https://www.google.com/search?q={}"'.format(query)
                    if sublime.platform() == 'windows':
                        subprocess.Popen("start chrome " + url, shell=True)
                    else:
                        subprocess.Popen("open " + url, shell=True)

                else:
                    if first_word in ['bing', 'bb' ]:
                        p = subprocess.Popen(
                            "PYTHONPATH=" + BINGCHAT_PATH + " "  + BING_PYTHON_EXEC_PATH + "  " + BINGCHAT_CMD ,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True,
                            shell=True
                        )
                        logging.debug('Bingchat launched')
                        out = p.stdout.readline()
                        # logging.debug('out: ' + out)
                        

                        input1 = " ".join(cont.split(" ")[1:])
                        out, errors = p.communicate(input= input1 )

                        # logging.debug('out: ' + out)
                        out = out[:-5]  # remove "#Me:"

                        out = out.replace("---waiting---", "").replace("---", "")

                        out = out.replace('\r', '')
                        self.view.replace(edit, line, out)


                    else: 
                        if sublime.platform() == 'windows':
                            path_prefix = "D:/_devs/Python01/ana3b/Scripts/"
                        else:
                            path_prefix = USER_PATH + "/conda3/miniconda3/envs/py38/bin/" 


                        p = subprocess.Popen(path_prefix + "howdoi " + cont,
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE,
                                             shell=True)
                        out, errors = p.communicate()




                        # Python 3 returns binary data, hence we have to decode it.
                        # Python 2 won't be affected by this decoding.
                        out = out.decode('utf-8')

                        # At least in Windows, out would contain carriage return
                        # characters (CR). We have to remove them in order to look
                        # properly.
                        out = out.replace('\r', '')

                        self.view.replace(edit, line, out)
