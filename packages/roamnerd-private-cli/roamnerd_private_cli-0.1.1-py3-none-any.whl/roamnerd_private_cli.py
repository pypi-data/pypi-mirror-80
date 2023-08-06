import argh
import os
import requests
from roamnerdMain import roamnerdMain
@argh.arg("files", help="File(s) to load.")
def main(verbose : "Display extra information about [[tags]]"=False,
            all : "Concatenate all results into one .md file with shared [[tags]]"=False,
            relevancy: "How many times an entity must appear before being written to output (Excludes Dates). Default 2."=2,
            categories: "Search by array of custom spacy tag categories. See https://spacy.io/api/annotation#named-entities for a full list"=["PERSON", "GPE", "LOC", "DATE"],
            *files):

    if len(files) == 0:
        print("Please provide .txt file(s)")
        return

    for file in files:
        assert file.endswith(".txt"), "One or more of your files is not a .txt file"
        assert os.path.isfile(file), "One or more of your files does not exist or is in a different directory"

    totalEntityCount = 0
    writtenFiles = 0
    numFiles = len(files)

    if all:
        with open("merge.txt", "w") as outfile:
            for file in files:
                with open(file, "r") as infile:
                    contents = infile.read()
                    outfile.write(contents)
            files = ["merge.txt"]


    for file in files:
        with open (file, 'r') as input:
            data = input.read()
            x = roamnerdMain({"text" : data, "categories" : ["PERSON", "LOC", "GPE", "NORP", "DATE", "ORG", "FAC", "WORK_OF_ART"], "model" : "en_core_web_sm", "relevancy" : relevancy})

        localEntityCount= sum(len(v) for v in x["tags"].values())
        totalEntityCount += localEntityCount

        with open(file[:-4]+ ".md", "w") as out:
            out.write(x["text"])
            writtenFiles += 1

            if verbose:
                allEnts = []
                for v in x["tags"].values():
                    allEnts = allEnts + v

                if len(allEnts) > 2:
                    if all:
                        print("\nFile 1 of 1: {0} files -> {1}.md".format(str(numFiles), file[:-4]))
                        os.remove("merge.txt")

                    else:
                        print("\nFile {0} of {1}: {2} -> {3}.md".format(str(writtenFiles), str(numFiles), file, file[:-4]))

                    print("Found entities: {0}, {1}, {2} and {3} more with relevancy {4}".format(allEnts[0], allEnts[1], allEnts[2], str(localEntityCount - 3), str(relevancy)))

    print("\nAnalyzed {0} files, found {1} named entities, wrote {2} file(s)\n".format(str(numFiles), str(totalEntityCount), str(writtenFiles)))
argh.dispatch_command(main)
