    subroutine fdr_rotation
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
    
    
    integer*2,dimension(8) :: fdr_archydro,fdr_whitebox
    integer*2 :: fdr_wb, fdr_hyd
	
    ! padrao prepro/hydrotools
	! 32  64  128
	! 16        1
	!  8   4    2    
    
    !padrão whitebox 
    ! 64 128   1
    ! 32   0   2
    ! 16   8   4
    
   
    !converte whitebox para archydro
    do j=1,nc
        do i=1,nl
            fdr_wb = dir(i,j)
            select case(fdr_wb)
            case(1)
                fdr_hyd = 128
            case(2)
                fdr_hyd = 1
            case(4)
                fdr_hyd = 2
            case(8)
                fdr_hyd = 4
            case(16)
                fdr_hyd = 8
            case(32)
                fdr_hyd = 16
            case(64)
                fdr_hyd = 32
            case(128)
                fdr_hyd = 64                
            end select
            ! atualiza
            dir(i,j) = fdr_hyd
            
        end do  
    end do
    
    
    end subroutine
    
    
    
    
