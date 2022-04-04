# -*- coding:utf-8 -*-
# Author: Kei Choi(hanul93@gmail.com)


import os
import re
import kernel
import kavutil


# -------------------------------------------------------------------------
# KavMain Ŭ����
# -------------------------------------------------------------------------
class KavMain:
    # ---------------------------------------------------------------------
    # init(self, plugins_path)
    # �÷����� ������ �ʱ�ȭ �Ѵ�.
    # �η°� : plugins_path - �÷����� ������ ��ġ
    #         verbose      - ����� ��� (True or False)
    # ���ϰ� : 0 - ����, 0 �̿��� �� - ����
    # ---------------------------------------------------------------------
    def init(self, plugins_path, verbose=False):  # �÷����� ���� �ʱ�ȭ
        self.p_http = re.compile(r'https?://')
        return 0  # �÷����� ���� �ʱ�ȭ ����
        
    # ---------------------------------------------------------------------
    # uninit(self)
    # �÷����� ������ �����Ѵ�.
    # ���ϰ� : 0 - ����, 0 �̿��� �� - ����
    # ---------------------------------------------------------------------
    def uninit(self):  # �÷����� ���� ����
        return 0  # �÷����� ���� ���� ����
        
    # ---------------------------------------------------------------------
    # scan(self, filehandle, filename, fileformat)
    # �Ǽ��ڵ带 �˻��Ѵ�.
    # �Է°� : filehandle  - ���� �ڵ�
    #         filename    - ���� �̸�
    #         fileformat  - ���� ����
    #         filename_ex - ���� �̸� (���� ���� ���� �̸�)
    # ���ϰ� : (�Ǽ��ڵ� �߰� ����, �Ǽ��ڵ� �̸�, �Ǽ��ڵ� ID) ���
    # ---------------------------------------------------------------------
    def scan(self, filehandle, filename, fileformat, filename_ex):  # �Ǽ��ڵ� �˻�
        try:
            mm = filehandle

            if mm[0:8] != '\x4c\x00\x00\x00\x01\x14\x02\x00':  # LNK ��� üũ
                raise ValueError
                
            flag = kavutil.get_uint32(mm, 0x14)
            
            off = 0x4c
            if flag & 0x0001 == 0x0001:  # HasLinkTargetIDList
                clid_mycom = '14001F50E04FD020EA3A6910A2D808002B30309D'.decode('hex')
                if mm[off+2:off+2+0x14] != clid_mycom:  # MyComputer
                    raise ValueError
                
                off += 2
                while True:
                    size = kavutil.get_uint16(mm, off)
                    if size == 0:
                        off += 2
                        break
                    if ord(mm[off+2]) == 0x32:
                        if mm[off+0xe:off+0xe+7].lower() != 'cmd.exe':
                            raise ValueError

                    off += size

            if flag & 0x0002 == 0x0002:  # HasLinkInfo
                off += kavutil.get_uint16(mm, off)
            
            if flag & 0x0004 == 0x0004:  # HasName
                size = kavutil.get_uint16(mm, off)
                off += (2 + (size * 2))
                
            if flag & 0x0008 == 0x0008:  # HasRelativePath
                size = kavutil.get_uint16(mm, off)
                cmd_path = mm[off+2:off+2+(size * 2):2].lower()

                # print cmd_path

                if cmd_path.find('cmd.exe') == -1:
                    raise ValueError
                off += (2 + (size * 2))
                
            if flag & 0x0010 == 0x0010:  # HasWorkingDir
                size = kavutil.get_uint16(mm, off)
                off += ( 2 + (size * 2))
                
            if flag & 0x0020 == 0x0020:  # HasArguments
                size = kavutil.get_uint16(mm, off)
                cmd_arg = mm[off+2:off+2+(size * 2):2].lower()
                cmd_arg = cmd_arg.replace('^', '')
                
                # print cmd_arg

                # �Ǽ��ڵ� ������ ���Ѵ�.
                if self.p_http.search(cmd_arg):
                    return True, 'Trojan.LNK.Agent.gen', 0, kernel.INFECTED
        except (IOError, ValueError):
            pass

        # �Ǽ��ڵ带 �߰����� �������� �����Ѵ�.
        return False, '', -1, kernel.NOT_FOUND

    # ---------------------------------------------------------------------
    # disinfect(self, filename, malware_id)
    # �Ǽ��ڵ带 ġ���Ѵ�.
    # �Է°� : filename    - ���� �̸�
    #        : malware_id - ġ���� �Ǽ��ڵ� ID
    # ���ϰ� : �Ǽ��ڵ� ġ�� ����
    # ---------------------------------------------------------------------
    def disinfect(self, filename, malware_id):  # �Ǽ��ڵ� ġ��
        try:
            # �Ǽ��ڵ� ���� ������� ���� ID ���� 0�ΰ�?
            if malware_id == 0:
                os.remove(filename)  # ���� ����
                return True  # ġ�� �Ϸ� ����
        except IOError:
            pass

        return False  # ġ�� ���� ����
        
    # ---------------------------------------------------------------------
    # listvirus(self)
    # ����/ġ�� ������ �Ǽ��ڵ��� ����Ʈ�� �˷��ش�.
    # ���ϰ� : �Ǽ��ڵ� ����Ʈ
    # ---------------------------------------------------------------------
    def listvirus(self):  # ���� ������ �Ǽ��ڵ� ����Ʈ
        vlist = list()  # ����Ʈ�� ���� ����

        vlist.append('Trojan.LNK.Agent.gen')  # ����/ġ���ϴ� �Ǽ��ڵ� �̸� ���

        return vlist         

    # ---------------------------------------------------------------------
    # getinfo(self)
    # �÷����� ������ �ֿ� ������ �˷��ش�. (������, ����, ...)
    # ���ϰ� : �÷����� ���� ����
    # ---------------------------------------------------------------------
    def getinfo(self):  # �÷����� ������ �ֿ� ����
        info = dict()  # ������ ���� ����

        info['author'] = 'Kei Choi'  # ������
        info['version'] = '1.0'      # ����
        info['title'] = 'LNK Scan Engine'  # ���� ����
        info['kmd_name'] = 'lnk'   # ���� ���� �̸�
        info['sig_num'] = 1  # ����/ġ�� ������ �Ǽ��ڵ� ��

        return info
