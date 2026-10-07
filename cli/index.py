import cmd

class ShinxShell(cmd.Cmd):
    prompt = 'shinx# '

    def do_start(self, arg):
        """Start Shinx""" # these are help prompts 
        print("Started the application")

    def do_stop(self, arg):
        """Stop Shinx"""
        print("Stopped the application")

if __name__ == "__main__":
    ShinxShell().cmdloop()