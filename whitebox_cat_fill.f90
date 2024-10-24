    subroutine cat_fill
    use MOD_PrePro_Prata
    implicit none

!  INCLUIR LINHAS ABAIXO EM 'PRATA_INPUT', APOS LEITURA DO FLOW DIRECTION
!
!   !@ ms: Rotate Flow Direction from 'WHITEBOX TOOLS'
!   write(*,*) "******************************************************************"
!   write(*,*) " DO YOU NEED TO CONVERT FLOW DIRECTION FROM WHITEBOX TO HYDRO?"
!   write(*,*) " (1) yes  (other) no"
!   write(*,*) "******************************************************************"
!   read(*,*) TRASH
!   if (TRASH == "1") then
!       write(*,*) "... adjusting flow direction"
!       call fdr_rotation
!   end if
    
	
    integer :: cod,codmax
    integer,allocatable :: pixel_count(:)
    
    !
    codmax = maxval(MINIBACIA)
    
   
    ! contagem de pixels por minibacia
    allocate(pixel_count(int(codmax)))
    pixel_count = 0    
    do j=1,nc
        do i=1,nl                
            cod = MINIBACIA(i,j)
            if (cod>0) then
                pixel_count(cod) = pixel_count(cod)+1
            end if
        end do
    end do
   
    ! verifica se todas as minibacias tem pelo menos 1 pixel
    !do i=1,codmax
    !    if (pixel_count(i)==0) then
    !        write(*,*)"ERRO: minibacia sem pixels - REMOVER",i
    !        write(*,*)
    !    end if
    !end do
    i = 1
    do while (i<=codmax)
        if (pixel_count(i)==0) then            
            write(*,*)"ERRO: minibacia sem pixels - REMOVENDO"
            write(*,*)i,codmax
            ! atualiza ids de bacias
            where (minibacia>i)
                rede = rede - 1
            end where
            where (minibacia>i)
                minibacia = minibacia - 1
            end where
            
            ! atualiza pixel_count
            do j=i,codmax
                pixel_count(i) = pixel_count(i+1)
            end do
            codmax = codmax - 1
            i = i - 1
        end if
        i = i + 1
    end do
    write(*,*) maxval(MINIBACIA)
    read(*,*)
    
    end subroutine
    
    
    
    
