import pexpect as pe
ssh_command = 'ssh -o "StrictHostKeyChecking no" {0}@{1} ls'.format(
    'stabrin',
    'clem'
    )

child = pe.spawnu(ssh_command)
print(child.after)
print(child.before)
child.expect(
    "{0}@{1}'s password:".format('stabrin', 'clem'),
    timeout=4
    )
print(child.after)
print(child.before)
