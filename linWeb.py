import socket
import sys 
import os
from use_archive import unzip_archive
from example import classify

def trydefineFunction():
	print("function define donnnnnnnnnnnnnnnnnnnnnnnnnnnnneeeeeeeeeeeeeee")

def classify_archive():
	archive = '/home/user/Desktop/Run_DIGITS_Locally/INSIDEv4.tar.gz'
	image_file = ['/home/user/Desktop/Run_DIGITS_Locally/tst.png'] 
	batch_size= None
	use_gpu= True
	tmpdir = unzip_archive(archive)

	caffemodel = None
	deploy_file = None
	mean_file = None
	labels_file = None
	for filename in os.listdir(tmpdir):
		full_path = os.path.join(tmpdir, filename)
		if filename.endswith('.caffemodel'):
		    caffemodel = full_path
		elif filename == 'deploy.prototxt':
		    deploy_file = full_path
		elif filename.endswith('.binaryproto'):
		    mean_file = full_path
		elif filename == 'labels.txt':
		    labels_file = full_path
		else:
		    print 'Unknown file:', filename

	assert caffemodel is not None, 'Caffe model file not found'
	assert deploy_file is not None, 'Deploy file not found'
	#print("NOt working: print Image file before call classify.\n")
	#print(image_file)
	resultLabel = classify(caffemodel, deploy_file, image_file,
		 mean_file=mean_file, labels_file=labels_file,
		batch_size=batch_size, use_gpu=use_gpu)
	return resultLabel 

if __name__ == '__main__':
	soc = socket.socket()
	host = "128.95.31.226"
	port = 2004
	soc.bind((host, port))
	soc.listen(10)
	print 'now listenning'

	conn, addr = soc.accept()
	print("Got connection from",addr)

	filename = open('tst.png','wb')

	while 1:	
		msg = conn.recv(1024)
		if not msg:
			break
		filename.write(msg)
	filename.close()
	soc.close()
	print 'finished'
	trydefineFunction()

	resultLabel = classify_archive()

	print(resultLabel)
	
	#print(addr[0])
	HOST = addr[0]    # The remote host
	PORT = 8080             # The same port as used by the server
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	print("sent")
	s.sendall(resultLabel)
	data = s.recv(1024)
	s.close()
	print 'Received', repr(data)
	


#os.system('python use_archive.py /home/user/Documents/Run_DIGITS_Locally/INSIDEv4.tar.gz /home/user/Documents/Run_DIGITS_Locally/tst.png')

