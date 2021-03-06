
from Bio import SeqIO
import os
import math
import cPickle

safe = False


map = dict()

curr_file = 'master.fasta'
for seq_record in SeqIO.parse(curr_file, "fasta"):
 curr_key = str(seq_record.seq)
 if (curr_key in map):
    map[curr_key]+= 1
 else:
    map[curr_key]=1 
if (safe):
  f = open('latest_dict.pickle','w')
  cPickle.dump(map,f)
  f.close()
  stat = open('dict_status.txt','a')
  stat.write('wrote:  final\n' )
  stat.close()

seq_count_pairs = map.items()
total_num_seq = sum( [ x[-1] for x in seq_count_pairs ] )
seq_count_pairs.sort(reverse=True,key=lambda pair: pair[-1])
count = 1
proper_name = os.getcwd().split('/')[-1]
outfile = open(proper_name + '_uniq.fasta','w')
summaryfile = open(proper_name + '_summary.csv','w')
summaryfile.write('seq#,distinct read,seq,read count,normalized read count (RPM)\n')
experiment_number = os.getcwd().split('/')[-1].split('_')[0]
for x in seq_count_pairs:
 
  outfile.write('>species' + str(count) + '_sample' + experiment_number +'of72_'+str(len(x[0]))+'bp\n')
  outfile.write(x[0]+'\n')
  normalized = 1000000 * float(x[1]) / total_num_seq
  summaryfile.write(str(count)+',>species' + str(count) + '_sample' +experiment_number +'of72_'+str(len(x[0]))+'bp,'+str(x[0])+','+str(x[1])+','+str(normalized)+'\n')
  count+=1
summaryfile.write(',total:'+str(total_num_seq)+',\n')
outfile.close()
summaryfile.close()
