

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os

print(os.path.dirname(__file__))
os.chdir(os.path.dirname(__file__))


def msg(i_click):
    global p_orig,xc1,yc1,xc2,yc2,lines_click
    if i_click==0:
        # if len(lines_click)!=0:
            # ax.lines.remove(lines_click[0])#error occurs. what is 'ArtistList' object??
        print('----------\nclick 1st calibration point')
        ax.set_title('click 1st calibration point')
        plt.show()
    elif i_click==1:
        lines_click=ax.plot(p_orig[0,0],p_orig[0,1],'r.')
        ax.set_title('input 1st calibration point')
        plt.show()
        temp=input('1st calib point (fmt:"x,y"):')
        [xc1,yc1]=np.array(temp.split(',')).astype(float)
        print('----------\nclick 2nd calibration point')
        # plt.plot(p_orig[0,0],p_orig[0,1],'r.')
        ax.set_title('click 2nd calibration point')
        plt.show()

    elif i_click==2:
        # ax.lines.remove(lines_click[0])#error occurs. what is 'ArtistList' object??
        lines_click=plt.plot(p_orig[0:2,0],p_orig[0:2,1],'r.')
        ax.set_title('input 2nd calibration point')
        plt.show()
        temp=input('2nd calib point (fmt:"x,y"):')
        [xc2,yc2]=np.array(temp.split(',')).astype(float)
        print(f'----------\nclick point {len(p_orig[:,0])-1}')
        ax.set_title(f'click point {len(p_orig[:,0])-1} (close this window->end clicking)')
        plt.show()

    else:
        print(f'----------\nclick point {len(p_orig[:,0])-1}')
        # plt.plot(p_orig[:2,0],p_orig[:2,1],'r.')
        # ax.lines.remove(lines_click[0])#error occurs. what is 'ArtistList' object??
        lines_click=plt.plot(p_orig[0:2,0],p_orig[0:2,1],'r.',p_orig[2:,0],p_orig[2:,1],'g.')
        ax.set_title(f'click point {len(p_orig[:,0])-1} (close this window->end clicking)')
        plt.show()
    print(' *Be sure to include left/right end point')
    print(' *click out of axis -> delete 1 point')
    return


def onclick(event):
    global p_orig,i_click,xc1,yc1,xc2,yc2,lines_click
    if event.xdata == None or event.ydata == None:
        ax.set_title('delete 1 point? (y/n)')
        plt.show()
        ans=input('delete 1 point? (y/n):')
        if ans=='y':
            print('delete data ',p_orig[-1,:])
            p_orig=p_orig[:-1,:]
            i_click-=1
            msg(i_click)
            return
        else:
            print('return')
            msg(i_click)
            return
    else:
        coord=np.array([[event.xdata, event.ydata]])
        p_orig = np.append(p_orig, coord, axis=0)
        print('add data ',coord)
        i_click+=1
        msg(i_click)
        return

if __name__ == "__main__":
    if not os.path.exists('fig'):
        print('fig directory not found. create fig directory.')
        print('put imagefiles in fig directory.')
        os.mkdir('fig')
    if not os.path.exists('data'):
        print('data directory not found. create data directory.')
        os.mkdir('data')

    while 1:
        files = os.listdir("./fig")
        for i_file in range(len(files)):
            print(f' {i_file} : {files[i_file]}')

        fignum=input('choose fig number:')
        savename_tail=input('tail of savename:')
        figname=files[int(fignum)]
        savename=files[int(fignum)].split('.')[0]+'_'+savename_tail
        print(f'figname:{figname}')
        print(f'savename:{savename}')


        #figname='u3posielev.png'
        #savename='temp


        ## initialize
        p_orig=np.zeros((0,2))
        i_click=0
        lines_click=[]

        ## show image
        im = Image.open(f'fig/{figname}')
        im_list = np.asarray(im)
        fig, ax = plt.subplots()
        plt.imshow(im_list)
        cid = fig.canvas.mpl_connect('button_press_event', onclick)
        msg(i_click)
        plt.show()


        # ## sort
        # p_orig_tmp=p_orig[2:,:]
        # inds_sort=np.argsort(p_orig_tmp[:,0])
        # p_orig_tmp=p_orig_tmp[inds_sort,:]
        # p_orig[2:,:]=p_orig_tmp
        
        
        ## linear transformation cf.30-5
        [Xc1,Yc1]=p_orig[0,:]
        [Xc2,Yc2]=p_orig[1,:]
        kx=(xc2-xc1)/(Xc2-Xc1)
        bx=(xc1*Xc2-xc2*Xc1)/(Xc2-Xc1)
        ky=(yc2-yc1)/(Yc2-Yc1)
        by=(yc1*Yc2-yc2*Yc1)/(Yc2-Yc1)

        p_trans=np.zeros(p_orig.shape)
        p_trans[:,0]=kx*p_orig[:,0]+bx
        p_trans[:,1]=ky*p_orig[:,1]+by

        
        
        
        print('------')
        print(p_orig)
        print(p_trans)
        
        
        np.savez(f'data/{savename}', p_orig=p_orig, p_trans=p_trans)
        np.savetxt(f'data/{savename}_orig.txt', p_orig[2:,:], fmt='%.7e')
        np.savetxt(f'data/{savename}_trans.txt', p_trans[2:,:], fmt='%.7e')

        plt.plot(p_trans[2:,0],p_trans[2:,1], '.')
        # plt.plot(p_trans[2:,0],p_trans[2:,1], 'o-')
        ax.set_title('p_trans plot (close this window->end checking)')
        plt.show()

        ans=input('Enter->next file, "e"->exit:')
        if ans=='e': break
        else: continue



