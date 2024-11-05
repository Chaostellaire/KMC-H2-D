program kinmonte
  !Will create a trajectory valid for case 1 
  implicit none
  
  !first declare usefull variables
  real :: GAMMA_ONE = 0.5
  real :: rdmval
  real :: dirTaken
  integer :: steps = 10000000
  integer, dimension(2) :: currPos = [0,0]
  integer :: i
  ! FINISHED


  call random_seed()
  OPEN(10,FILE = './traj.txt')
  WRITE(10,*) currPos
  do i = 1, steps, 1
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
    WRITE(10,*) currPos
  end do
  
end program kinmonte
  
!subroutine name(input)
  !argument type, intent(inout) :: input
  
!end subroutine name
