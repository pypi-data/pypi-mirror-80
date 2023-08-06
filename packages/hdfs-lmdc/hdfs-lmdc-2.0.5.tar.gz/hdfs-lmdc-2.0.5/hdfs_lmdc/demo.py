# from hdfs import HDFSWrapper
#
# def main():
#     hdfs_name_services = "Namenode1"
#     user = "hdfs"
#     hdfs_replication ="1"
#     hdfs_host_services = "sandbox-hdp.hortonworks.com:8020"
#
#     my_client = HDFSWrapper.hdfs_connect_withoutlogin(hdfs_name_services, user, hdfs_replication, hdfs_host_services)
#     print("Status conection:",my_client.getClient())
#
# # Os testes estan feitos utilizando a imagen do docker do  Pdf-Extractor
# if __name__=="__main__":
#     main()
from hdfs_lmdc.hdfs import HDFSWrapperClient

a = HDFSWrapperClient.load_from_envs()
# a.mkdir("/tmp/oi3")
# a.upload("/home/thaylon/c.jpg", "/tmp")
# print(a.glob("/tmp"))
# result = a.read_image("/tmp/c.jpg")
# print(a.read_txt("/tmp/producao-terra-2014-1sem.csv"))
# print(a.download("/tmp/c.jpg", "/tmp")[1].erro)