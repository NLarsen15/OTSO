subroutine VecScale(A, Vector, VectorNew)
implicit none
real(8) :: A
real(8) :: Vector(3), VectorNew(3)


VectorNew(1) = Vector(1)*A
VectorNew(2) = Vector(2)*A
VectorNew(3) = Vector(3)*A

end subroutine VecScale

subroutine VecCross(Vector1, Vector2, VectorNew)
implicit none
real(8) :: Vector1(3),Vector2(3), VectorNew(3)
    
    
VectorNew(1) = (Vector1(2)*Vector2(3) - Vector1(3)*Vector2(2))
VectorNew(2) = (Vector1(3)*Vector2(1) - Vector1(1)*Vector2(3))
VectorNew(3) = (Vector1(1)*Vector2(2) - Vector1(2)*Vector2(1))
    
end subroutine VecCross

subroutine VecDot(Vector1, Vector2, DotProduct)
implicit none
real(8),intent(in) :: Vector1(3),Vector2(3)
real(8),intent(out) :: DotProduct
                
DotProduct = Vector1(1)*Vector2(1) + Vector1(2)*Vector2(2) + Vector1(3)*Vector2(3)
        
end subroutine VecDot

subroutine VecAddition(Vector1, Vector2, VectorNew)
implicit none
real(8) :: Vector1(3),Vector2(3), VectorNew(3)
            
            
VectorNew(1) = Vector1(1)+Vector2(1) 
VectorNew(2) = Vector1(2)+Vector2(2)
VectorNew(3) = Vector1(3)+Vector2(3)
            
end subroutine VecAddition