import os
import json
import subprocess
from pprint import pprint
import sys, getopt, os
import yaml

def imageCheck(image):
    proc = subprocess.Popen("wsl -d %s --exec uname" % (image), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while proc.poll() is None:
        continue
    imageExitCode = proc.wait()
    return imageExitCode

def cmdExit(command,image):
    cmdStr = 'wsl -d %s --exec %s' % (image, command)
    print("wslExec (image: %s): %s" % (image, command))
    proc = subprocess.Popen(cmdStr, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while proc.poll() is None:
        # print(str(proc.stdout.readline()))
        continue
    commandResult = proc.wait()
    return { 'exit_code': commandResult }

def executeSteps(steps,image):
    stats = []
    exits = []
    completed = {}
    for k,v in enumerate(steps):
        commandRunner = cmdExit(v, image)
        step = {}
        step['id'] = k
        step['exit_code'] = commandRunner['exit_code']
        step['cmd'] = v
        stats.append(step)
        exits.append(commandRunner['exit_code'])
        if commandRunner['exit_code'] == 0:
            print("✔️: %s\n" % (v))
        else:
            print("❌: %s\n" % (v))
    completed['completions'] = "%s/%s" % (exits.count(0), len(exits))
    stats.append(completed)
    return stats

def manifestRead(manifestPath):
    try:
        with open(manifestPath, "rt") as manifest_json:
            manifest = yaml.safe_load(manifest_json)
        return manifest
    except OSError as e:
        return e

def definePipeline(manifestPath):
    manifest = manifestRead(manifestPath)
    if isinstance(manifest, OSError) == True:
        print(manifest)
        exit(2)
    pipeline = []
    for stage in manifest['stages']:
        stage_data = {}
        stage_data['name'] = stage['name']
        imageStatus = imageCheck(stage['image'])
        if imageStatus == 0:
            job = executeSteps(stage['steps'], stage['image'])
            print("🔔: %s completed."  % (stage['name']))
            stage_data['stages_run'] = job
        else:
            stage_data['stages_run'] = [{ "completions": "0/0, Image %s Unavailable: %s" % (stage['image'], imageStatus) }]
        pipeline.append(stage_data)
    return pipeline
    
def runPipeline(pipeline_definition):
    pipeline = definePipeline(pipeline_definition)
    
    print("Pipeline completed:\n")
    for job in pipeline:
        print("🧾 Report: " + job['name'] + "...\n")
        for j in job['stages_run']:
            if 'completions' in j:
                pprint(j)
                print("\n")
    return "Completed."

# if __name__ == "__main__":
#     exit(main(pipeline_definition))


def main():

    try:
        opts, args = getopt.getopt(sys.argv[1:],"hi:o:", ["pipeline=",""])
    except getopt.GetoptError:
        print("-p 'pipeline'")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-p", "--pipeline"):
            pipeline = arg
        # elif opt in ("-m", "--mode"):
        #     mode = arg

    print(runPipeline(pipeline))