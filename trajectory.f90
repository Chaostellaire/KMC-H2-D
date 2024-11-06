program main

real :: GAMMA_ONE = 0.5
integer :: STEPS = 10000000

call kinmonte(STEPS, GAMMA_ONE,1)


end program main

subroutine kinmonte(STEPS, GAMMA_ONE,N)
  !Will create a trajectory valid for case 1 
  implicit none
  
  !first declare usefull variables
  real,intent(in) :: GAMMA_ONE 
  real :: rdmval
  real :: dirTaken
  integer :: N
  integer, intent(in) :: STEPS 
  integer, dimension(2) :: currPos = [0,0]
  integer, dimension(STEPS+1,2) :: resultPos
  integer :: i
  character(512) :: PathStr
  ! FINISHED

  !Initialise the random seed
  call random_seed()
  !first position :
  resultPos(1,:) = currPos

  !Do loop.
  do i = 2, STEPS+1, 1
    !random val to know if we do axis or diag jump
    call random_number(rdmval)

    if (rdmval < GAMMA_ONE) then
      !We choose to jump along an axis
      call random_number(dirTaken)
      if (dirTaken*4 < 1) then
        ! +x
       currPos = [currPos(1)+1,currPos(2)]
      else if (dirTaken*4 < 2) then
        ! -x
        currPos = [currPos(1)-1,currPos(2)]
      else if (dirTaken*4 < 3) then
        ! +y
        currPos = [currPos(1),currPos(2)+1]
      else
        ! -y
        currPos = [currPos(1),currPos(2)-1]
      end if 

    else
      !We choose to jump along diagonals
      call random_number(dirTaken)

      if (dirTaken*4 < 1) then
        ! +x+y
        currPos = [currPos(1)+1,currPos(2)+1]
      else if (dirTaken*4 < 2) then
        ! -x+y
        currPos = [currPos(1)-1,currPos(2)+1]
      else if (dirTaken*4 < 3) then
        ! +x-y
        currPos = [currPos(1)+1,currPos(2)-1]
      else
        ! -x-y
        currPos = [currPos(1)-1,currPos(2)-1]
      end if
    end if

  resultPos(i,:) = currPos
  end do

  !write results
  PathStr = MakeString(GAMMA_ONE, STEPS, "traj",1)
  OPEN(10,FILE = MakeString(GAMMA_ONE, STEPS, "traj", 1,1))
  WRITE (10, currPos)

  
end subroutine kinmonte

function MakeString(GAMMA_ONE, STEPS, strTY,Model, N) result(PathStr)
  implicit none
  real, intent(in) :: GAMMA_ONE
  integer, intent(in) :: STEPS
  character(4), intent(in) :: strTY
  integer, intent(in) :: N
  integer, intent(in) :: Model


  character(50) :: strGAM, strSTP, strMod, strN
  character(502) :: PathStr 

  ! create first part with real part
  write(strGAM, '(f5.2)') GAMMA_ONE
  !create part with int
  write(strSTP, '(i16)') STEPS
  write(strMod, '(i1)') Model
  write(strN, '(i3)') N

  PathStr = "GAMMA1_SHARE_"//strGAM//"/model"//strMod//"_"//strSTP//"_"//strTY//"_"//strN//".txt"
end function MakeString

function MQV(STEPS,GAMMA_ONE, KSTEP) result(mqvres)
  implicit none
  
  integer, intent(in) :: STEPS
  real, intent(in) :: GAMMA_ONE
  integer, intent(in) :: KSTEP
  real :: mqvres
  integer :: i

  !read our trajectory
  do i = 1, STEPS-KSTEP


  end do
  
end function MQV 
