import re
with open('/home/em-transfer-user/projects/2019_11_06_ULTIMATE_TEST_rbx_thr_thld10_update_thr_krios1_count_K2/sp_auto_v1.3/005_substack_transphire.log', 'r') as read:
    content = read.read()
print(content)
shrink_ratio = re.search('ISAC shrink ratio\s*:\s*(0\.\d+)', content, re.MULTILINE).groups()
n_particles = re.search('Accounted particles\s*:\s*(\d+)', content, re.MULTILINE).groups()
n_classes = re.search('Provided class averages\s*:\s*(\d+)', content, re.MULTILINE).groups()
print('AASDF')
#match = re.match('.*ISAC shrink ratio\s*:\s*(0\.\d*).*Accounted in fullstack\s*:\s*(\d+).*Provided class averages\s*:\s*(\d+).*', content, re.MULTILINE)
print(shrink_ratio)
print(n_particles)
print(n_classes)
