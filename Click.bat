@echo off
title ��ȡ����ԱȨ��
mode con cols=100 lines=20
color 3f

:: ��ʼ��ȡ����ԱȨ��
setlocal
set uac=~uac_permission_tmp_%random%
md "%SystemRoot%\system32\%uac%" 2>nul
if %errorlevel%==0 ( rd "%SystemRoot%\system32\%uac%" >nul 2>nul ) else (
    echo set uac = CreateObject^("Shell.Application"^)>"%temp%\%uac%.vbs"
    echo uac.ShellExecute "%~s0","","","runas",1 >>"%temp%\%uac%.vbs"
    echo WScript.Quit >>"%temp%\%uac%.vbs"
    "%temp%\%uac%.vbs" /f
    del /f /q "%temp%\%uac%.vbs" & exit )
endlocal
:: ��ɻ�ȡ,������Կ�ʼд���Լ��Ĵ�����

echo.
echo ԭ���ȳ�����ϵͳĿ¼����ʱ�½�һ���ļ��У����ѻ�ȡ����ԱȨ�޻���������XP�Ȳ���Ҫ����ԱȨ�޵�
echo       ��ϵͳʱ���ǿ����½��ɹ��ģ���ʱֻ��ɾ�������ʱ�½����ļ��оͺ��ˣ�����ͨ������һ����ʱ
echo       vbs�ű���ȡ����ԱȨ�ޣ�Ȼ����ɾ�������ʱvbs�ű��ļ���
echo.
echo ��ʾ������ȡ����ԱĿ¼���������������Ŀ¼�ᷢ���仯��Ϊ��֤Ŀ¼׼ȷ��
echo       ��ͨ�� cd �л�Ŀ¼,����cd /d %%~dp0���л�������������Ŀ¼
echo.
echo ��ǰ����Ŀ¼�� %cd%\
echo ����������Ŀ¼��%~dp0
echo.
echo �����л�������������Ŀ¼
echo cd /d %%~dp0
echo.

cd /d %~dp0

echo ��ǰ����Ŀ¼�� %cd%\
echo ����������Ŀ¼��%~dp0	

python "D:\PyCharm Workspace\commonUtils\TempUtils\Click.py"

pause
exit